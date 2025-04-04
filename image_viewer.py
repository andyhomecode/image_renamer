import pygame
import os
from pathlib import Path
from PIL import Image
from datetime import datetime
from renamer import build_new_filename  # Import the function
from exif_reader import get_image_date, get_gps_coordinates  # Import GPS and date extraction
from geolocator import reverse_geocode  # Import reverse geocoding

class ImageViewer:
    def __init__(self, image_path, change_entry):
        self.image_path = image_path
        self.change_entry = change_entry  # Dictionary containing original, proposed, and delete flag
        self.screen = None
        self.running = True
        self.description = change_entry.get("description", "")  # Initialize description from change_entry
        self.prefix = change_entry.get("prefix", "")  # Initialize prefix from change_entry
        self.include_location = change_entry.get("include_location", True)  # Initialize location toggle
        self.use_prefix = change_entry.get("use_prefix", True)  # Initialize prefix toggle
        self.show_date = change_entry.get("show_date", True)  # Initialize date toggle
        self.show_overlay = True  # Initialize overlay visibility toggle
        self.done = False
        self.city = change_entry.get("city", "")  # Initialize city from change_entry
        self.location_edited = change_entry.get("location_edited", False)  # Track if location was manually edited
        self.date = change_entry.get("date", None)  # Initialize date from change_entry
        self.editing_field = "description"  # Default to editing the description
        self.date_text = self.date.strftime('%Y %m %d') if self.date else ""  # Editable date text
        self.fields = ["date", "prefix", "location", "description"]  # Ordered list of fields
        self.previous_image = False  # Flag to indicate moving to the previous image
        self.next_image = False  # Flag to indicate moving to the next image

        # Load metadata for the current image if not already loaded or manually edited
        if not self.date or (not self.city and not self.location_edited):
            self.load_image_metadata()

    def show_image(self):
        pil_image = Image.open(self.image_path).convert('RGB')

        # Get screen dimensions
        screen_width, screen_height = self.screen.get_size()

        # Resize image to fit the screen dimensions
        pil_image.thumbnail((screen_width, screen_height))
        image = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)
        image_rect = image.get_rect(center=(screen_width // 2, screen_height // 2))

        self.screen.fill((30, 30, 30))  # Clear screen with dark gray
        self.screen.blit(image, image_rect)

        if self.show_overlay:  # Only draw the overlay if it is visible
            self.draw_overlay()

        pygame.display.flip()

    def draw_overlay(self):
        # Translucent background
        overlay_rect = pygame.Rect(10, 30, self.screen.get_width() - 20, 250)
        overlay_surface = pygame.Surface((overlay_rect.width, overlay_rect.height), pygame.SRCALPHA)
        overlay_surface.fill((0, 0, 0, 150))  # Black with 150 alpha (translucent)
        self.screen.blit(overlay_surface, (overlay_rect.x, overlay_rect.y))

        # Overlay text
        def add_cursor(text, field_name):
            """Add a block cursor to the text if the field is being edited."""
            if self.editing_field == field_name:
                return text + "_"
            return text

        def get_text_color(field_name):
            """Return white for the editing field, gray for others."""
            return (255, 255, 255) if self.editing_field == field_name else (150, 150, 150)

        date_text = self.date_text if self.editing_field == "date" else (self.date.strftime('%Y %m %d') if self.date else 'Unknown')
        lines = []
        # Always display the date field, but indicate whether it is included in the filename
        lines.append((f"[F1] Date {'[EXCLUDED]' if not self.show_date else ''} {'[EDITING]' if self.editing_field == 'date' else ''}: {add_cursor(date_text, 'date')}", "date"))
        lines.append((f"[F2] Prefix {'[HIDDEN]' if not self.use_prefix else ''} {'[EDITING]' if self.editing_field == 'prefix' else ''}: {add_cursor(self.prefix, 'prefix')}", "prefix"))
        lines.append((f"[F3] Location {'[HIDDEN]' if not self.include_location else ''} {'[EDITING]' if self.editing_field == 'location' else ''}: {add_cursor(self.city, 'location')}", "location"))
        lines.append((f"Description {'[EDITING]' if self.editing_field == 'description' else ''}: {add_cursor(self.description, 'description')}", "description"))

        if self.change_entry["delete"]:
            lines.append(("Filename: ***DELETED***", None))
        else:
            final_name = self.build_final_filename()
            lines.append((f"Final Name: {final_name}", None))
        lines.append(("[shift-F3] to reload geo  [F4] Show/Hide Overlay   [Enter] Confirm   [Del] to Delete", None))

        font = pygame.font.SysFont(None, int(24))  # Increase font size by 20%
        for i, (line, field_name) in enumerate(lines):
            text_color = get_text_color(field_name) if field_name else (255, 255, 255)  # Default to white for non-editable lines
            text_surface = font.render(line, True, text_color)
            self.screen.blit(text_surface, (20, 40 + i * 36))  # Adjust line spacing proportionally

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            print(f"Key pressed: {event.key}")  # Debugging: Check if keypresses are detected
            if event.key == pygame.K_F1:  # Toggle inclusion of date in the filename
                self.show_date = not self.show_date
            elif event.key == pygame.K_F2:  # Toggle inclusion of prefix in the filename
                self.use_prefix = not self.use_prefix
            elif event.key == pygame.K_F3 and not (event.mod & pygame.KMOD_SHIFT):  # Toggle inclusion of location
                self.include_location = not self.include_location
            elif event.key == pygame.K_F3 and (event.mod & pygame.KMOD_SHIFT):  # Reload geolocation
                gps = get_gps_coordinates(self.image_path)  # Get GPS coordinates
                if gps:
                    self.city = reverse_geocode(*gps) or ""  # Reload geolocation
                    self.location_edited = False  # Reset manual edit flag
                    print(f"Geolocation reloaded: {self.city}")  # Debugging
            elif event.key == pygame.K_F4:  # Toggle overlay visibility
                self.show_overlay = not self.show_overlay
            elif event.key == pygame.K_DELETE:  # Toggle delete/undelete for the current file
                if self.change_entry["delete"]:
                    self.change_entry["delete"] = False
                    self.change_entry["proposed"] = self.change_entry["original"]
                else:
                    self.change_entry["delete"] = True
                    self.change_entry["proposed"] = "***DELETED***"
            elif event.key == pygame.K_UP:  # Move to the previous field
                current_index = self.fields.index(self.editing_field)
                self.editing_field = self.fields[(current_index - 1) % len(self.fields)]
                print(f"Editing field changed to: {self.editing_field}")  # Debugging
                if self.editing_field == "date":
                    self.date_text = self.date.strftime('%Y %m %d') if self.date else ''  # Initialize editable date text
            elif event.key == pygame.K_DOWN:  # Move to the next field
                current_index = self.fields.index(self.editing_field)
                if self.editing_field == "date":  # Update the date field before leaving
                    try:
                        self.date = datetime.strptime(self.date_text, '%Y %m %d')  # Validate and set the date
                    except ValueError:
                        print("Invalid date format. Keeping the previous date.")
                self.editing_field = self.fields[(current_index + 1) % len(self.fields)]
                print(f"Editing field changed to: {self.editing_field}")  # Debugging
            elif event.key in [pygame.K_RETURN, pygame.K_RIGHT]:  # Save changes and move to the next image
                self.done = True
                self.next_image = True
            elif event.key == pygame.K_LEFT:  # Save changes and move to the previous image
                self.done = True
                self.previous_image = True
            elif self.editing_field == "date":  # Handle date editing
                if event.key == pygame.K_RETURN:
                    try:
                        self.date = datetime.strptime(self.date_text, '%Y %m %d')  # Validate and set the date
                    except ValueError:
                        print("Invalid date format. Use YYYY MM DD.")
                    self.editing_field = "description"  # Revert to editing description
                elif event.key == pygame.K_BACKSPACE:
                    self.date_text = self.date_text[:-1]  # Remove the last character
                elif event.unicode and event.unicode.isprintable():
                    self.date_text += event.unicode  # Add the typed character
            elif self.editing_field == "prefix":  # Handle prefix editing
                if event.key == pygame.K_RETURN:
                    self.editing_field = "description"  # Revert to editing description
                elif event.key == pygame.K_BACKSPACE:
                    self.prefix = self.prefix[:-1]
                elif event.unicode and event.unicode.isprintable():
                    self.prefix += event.unicode
            elif self.editing_field == "location":  # Handle location editing
                if event.key == pygame.K_RETURN:
                    self.editing_field = "description"  # Revert to editing description
                elif event.key == pygame.K_BACKSPACE:
                    self.city = self.city[:-1]
                    self.location_edited = True  # Mark location as manually edited
                elif event.unicode and event.unicode.isprintable():
                    self.city += event.unicode
                    self.location_edited = True  # Mark location as manually edited
            elif self.editing_field == "description":  # Handle description editing
                if event.key == pygame.K_RETURN:
                    self.done = True  # Confirm and proceed
                elif event.key == pygame.K_BACKSPACE:
                    self.description = self.description[:-1]  # Remove the last character
                elif event.unicode and event.unicode.isprintable():
                    self.description += event.unicode  # Add the typed character

            # Refresh the overlay after handling the event
            self.show_image()

    def load_image_metadata(self):
        """Load metadata (date, location, and refresh file name) for the current image."""
        self.date = get_image_date(self.image_path)  # Get the image date
        self.date_text = self.date.strftime('%Y %m %d') if self.date else ""  # Preload editable date text
        if not self.location_edited:  # Only load geolocated city if not manually edited
            gps = get_gps_coordinates(self.image_path)  # Get GPS coordinates
            self.city = reverse_geocode(*gps) if gps else ""  # Reverse geocode the location

    def build_final_filename(self):
        """Build the final filename based on the current state."""
        return build_new_filename(
            self.date if self.show_date else None,
            self.prefix if self.use_prefix else "",
            self.city if self.include_location else "",
            self.description.strip(),
            Path(self.image_path).suffix.lower()
        )

    def handle_current_image(self):
        # Update the proposed name or delete flag for the current image
        if self.done:
            if self.change_entry["delete"]:
                self.change_entry["proposed"] = "***DELETED***"
            else:
                self.change_entry["proposed"] = self.build_final_filename()
                self.change_entry["description"] = self.description.strip()
                self.change_entry["prefix"] = self.prefix.strip()
                self.change_entry["city"] = self.city.strip()
                self.change_entry["date"] = self.date
                self.change_entry["include_location"] = self.include_location
                self.change_entry["use_prefix"] = self.use_prefix
                self.change_entry["show_date"] = self.show_date
                self.change_entry["location_edited"] = self.location_edited  # Save manual edit status
            self.done = False  # Reset for the next image
            self.description = ""

    def get_changes(self):
        # Return the updated change entry
        return self.change_entry

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.show_image()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_event(event)

            if self.done:
                self.handle_current_image()
                if self.previous_image or self.next_image:
                    break  # Exit the loop to signal navigation to another image
                self.show_image()

        pygame.quit()

if __name__ == "__main__":
    image_path = "./photos/sample.jpg"  # Change this to your image file
    change_entry = {"original": "sample.jpg", "proposed": "sample.jpg", "delete": False}
    viewer = ImageViewer(image_path, change_entry)
    viewer.run()
    print(viewer.get_changes())
