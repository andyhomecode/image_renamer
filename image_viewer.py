import pygame
import os
from pathlib import Path
from PIL import Image
from datetime import datetime
from renamer import build_new_filename  # Import the function
from exif_reader import get_image_date, get_gps_coordinates  # Import GPS and date extraction
from geolocator import reverse_geocode  # Import reverse geocoding

# Global variables for prefix and location toggle
global_prefix = ""
global_include_location = True
global_use_prefix = True

# Global variables for toggling visibility
global_show_date = True
global_show_prefix = True
global_show_location = True

# Global variable for overlay visibility
global_show_overlay = True

class ImageViewer:
    def __init__(self, folder_path):
        global global_prefix, global_include_location, global_use_prefix, global_show_date, global_show_prefix, global_show_location, global_show_overlay
        self.folder = Path(folder_path)
        self.images = sorted([f for f in self.folder.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
        self.index = 0
        self.screen = None
        self.running = True
        self.description = ""
        self.prefix = global_prefix  # Initialize with global prefix
        self.include_location = global_include_location  # Initialize with global location toggle
        self.use_prefix = global_use_prefix  # Initialize with global prefix toggle
        self.show_date = global_show_date  # Initialize with global date toggle
        self.show_prefix = global_show_prefix  # Initialize with global prefix visibility toggle
        self.show_location = global_show_location  # Initialize with global location visibility toggle
        self.show_overlay = global_show_overlay  # Initialize with global overlay visibility toggle
        self.done = False
        self.city = ""  # Placeholder for city name
        self.date = None  # Placeholder for image date
        self.editing_field = "description"  # Default to editing the description
        self.date_text = ""  # Editable date text
        self.fields = ["date", "prefix", "location", "description"]  # Ordered list of fields

    def show_image(self):
        img_path = self.images[self.index]
        pil_image = Image.open(img_path).convert('RGB')

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
        # Use build_new_filename to calculate the final name
        valid_date = self.date if self.date else datetime.now()  # Fallback to current date if self.date is None
        final_name = build_new_filename(
            valid_date if self.show_date else None,  # Include date if toggled on
            self.prefix if self.use_prefix else "",  # Include prefix if toggled on
            self.city if self.include_location else "",  # Include location if toggled on
            self.description.strip(),  # Include description
            ".jpg"  # Default extension for display purposes
        )

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
        if self.show_prefix:
            lines.append((f"[F2] Prefix {'[HIDDEN]' if not self.use_prefix else ''} {'[EDITING]' if self.editing_field == 'prefix' else ''}: {add_cursor(self.prefix, 'prefix')}", "prefix"))
        if self.show_location:
            lines.append((f"[F3] Location {'[HIDDEN]' if not self.include_location else ''} {'[EDITING]' if self.editing_field == 'location' else ''}: {add_cursor(self.city, 'location')}", "location"))
        lines.append((f"Description {'[EDITING]' if self.editing_field == 'description' else ''}: {add_cursor(self.description, 'description')}", "description"))
        lines.append((f"Final Name: {final_name}", None))
        lines.append(("[F4] Show/Hide Overlay   [Enter] Confirm", None))

        font = pygame.font.SysFont(None, int(24))  # Increase font size by 20%
        for i, (line, field_name) in enumerate(lines):
            text_color = get_text_color(field_name) if field_name else (255, 255, 255)  # Default to white for non-editable lines
            text_surface = font.render(line, True, text_color)
            self.screen.blit(text_surface, (20, 40 + i * 36))  # Adjust line spacing proportionally

    def handle_event(self, event):
        global global_prefix, global_include_location, global_use_prefix, global_show_date, global_show_prefix, global_show_location, global_show_overlay
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:  # Toggle inclusion of date in the filename
                self.show_date = not self.show_date
                global_show_date = self.show_date  # Update global toggle
            elif event.key == pygame.K_F2:  # Toggle inclusion of prefix in the filename
                self.use_prefix = not self.use_prefix
                global_use_prefix = self.use_prefix  # Update global toggle
            elif event.key == pygame.K_F3:  # Toggle inclusion of location in the filename
                self.include_location = not self.include_location
                global_include_location = self.include_location  # Update global toggle
            elif event.key == pygame.K_F4:  # Toggle overlay visibility
                self.show_overlay = not self.show_overlay
                global_show_overlay = self.show_overlay  # Update global toggle
            elif event.key == pygame.K_UP:  # Move to the previous field
                current_index = self.fields.index(self.editing_field)
                self.editing_field = self.fields[(current_index - 1) % len(self.fields)]
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
                    global_prefix = self.prefix  # Update global prefix
                elif event.key == pygame.K_BACKSPACE:
                    self.prefix = self.prefix[:-1]
                elif event.unicode and event.unicode.isprintable():
                    self.prefix += event.unicode
            elif self.editing_field == "location":  # Handle location editing
                if event.key == pygame.K_RETURN:
                    self.editing_field = "description"  # Revert to editing description
                elif event.key == pygame.K_BACKSPACE:
                    self.city = self.city[:-1]
                elif event.unicode and event.unicode.isprintable():
                    self.city += event.unicode
            elif self.editing_field == "description":  # Handle description editing
                if event.key == pygame.K_RETURN:
                    self.done = True  # Confirm and proceed
                elif event.key == pygame.K_BACKSPACE:
                    self.description = self.description[:-1]  # Remove the last character
                elif event.unicode and event.unicode.isprintable():
                    self.description += event.unicode  # Add the typed character
            else:  # Handle other events
                if event.key == pygame.K_RETURN:
                    self.done = True
                elif event.key == pygame.K_RIGHT:
                    self.index = (self.index + 1) % len(self.images)
                    self.load_image_metadata()  # Reload metadata for the new image
                    self.show_image()
                    self.done = False
                    self.description = ""
                elif event.key == pygame.K_LEFT:
                    self.index = (self.index - 1) % len(self.images)
                    self.load_image_metadata()  # Reload metadata for the new image
                    self.show_image()
                    self.done = False
                    self.description = ""
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    # Handle Shift+F4 and Shift+F1 for toggling visibility
                    if event.mod & pygame.KMOD_SHIFT:
                        if event.key == pygame.K_F4:  # Show/Hide prefix
                            self.use_prefix = not self.use_prefix
                            global_use_prefix = self.use_prefix  # Update global toggle
                        elif event.key == pygame.K_F1:  # Show/Hide location
                            self.include_location = not self.include_location
                            global_include_location = self.include_location  # Update global toggle

    def load_image_metadata(self):
        """Load metadata (date, location, and refresh file name) for the current image."""
        image_path = self.get_current_image_path()
        self.date = get_image_date(image_path)  # Get the image date
        gps = get_gps_coordinates(image_path)  # Get GPS coordinates
        self.city = reverse_geocode(*gps) if gps else ""  # Reverse geocode the location
        self.images[self.index] = image_path  # Refresh the file name in case it was changed

    def get_current_image_path(self):
        return self.images[self.index]

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
                print("Final Description:", self.description.strip())
                print("Include Location:", self.include_location)
                print("Use Prefix:", self.use_prefix)
                self.done = False  # Reset for the next image

        pygame.quit()

if __name__ == "__main__":
    viewer = ImageViewer("./photos")  # Change this to your image folder
    viewer.run()
