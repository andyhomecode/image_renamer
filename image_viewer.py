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

class ImageViewer:
    def __init__(self, folder_path):
        global global_prefix, global_include_location, global_use_prefix
        self.folder = Path(folder_path)
        self.images = sorted([f for f in self.folder.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
        self.index = 0
        self.screen = None
        self.running = True
        self.description = ""
        self.prefix = global_prefix  # Initialize with global prefix
        self.include_location = global_include_location  # Initialize with global location toggle
        self.use_prefix = global_use_prefix  # Initialize with global prefix toggle
        self.done = False
        self.city = ""  # Placeholder for city name
        self.date = None  # Placeholder for image date
        self.editing_field = None  # Tracks which field is being edited ("prefix", "location", or "description")

    def show_image(self):
        img_path = self.images[self.index]
        pil_image = Image.open(img_path).convert('RGB')

        # Reserve space for a top bar (e.g., 50 pixels)
        screen_width, screen_height = self.screen.get_size()
        overlay_height = 50
        image_area = pygame.Rect(0, overlay_height, screen_width, screen_height - overlay_height)

        # Resize image to fit image_area
        pil_image.thumbnail((image_area.width, image_area.height))
        image = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)
        image_rect = image.get_rect(center=image_area.center)

        self.screen.fill((30, 30, 30))  # Clear screen with dark gray
        self.screen.blit(image, image_rect)

        # Draw overlay bar
        font = pygame.font.SysFont(None, 16) 
        text_surface = font.render(f"{img_path.name} ({self.index+1}/{len(self.images)})", True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))

        self.draw_overlay()
        pygame.display.flip()

    def draw_overlay(self):
        # Use build_new_filename to calculate the final name
        final_name = build_new_filename(
            self.date or datetime.now(),  # Use current date if not set
            self.city if self.include_location else "",
            f"{self.prefix if self.use_prefix else ''} {self.description}".strip(),
            ".jpg"  # Default extension for display purposes
        )

        # Translucent background
        overlay_rect = pygame.Rect(10, 30, self.screen.get_width() - 20, 250)
        overlay_surface = pygame.Surface((overlay_rect.width, overlay_rect.height), pygame.SRCALPHA)
        overlay_surface.fill((0, 0, 0, 150))  # Black with 150 alpha (translucent)
        self.screen.blit(overlay_surface, (overlay_rect.x, overlay_rect.y))

        # Overlay text
        lines = [
            f"F4 Prefix {'[HIDDEN]' if not self.use_prefix else ''} {'[EDITING]' if self.editing_field == 'prefix' else ''}: {self.prefix}",
            f"F1 Location {'[HIDDEN]' if not self.include_location else ''} {'[EDITING]' if self.editing_field == 'location' else ''}: {self.city}",
            f"Description {'[EDITING]' if self.editing_field == 'description' else ''}: {self.description}",
            f"Final Name: {final_name}",
            "[Shift+F4] Show/Hide Prefix   [Shift+F1] Show/Hide Location   [Enter] Confirm"
        ]

        font = pygame.font.SysFont(None, int(14 * 1.2))  # Increase font size by 20%
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (20, 40 + i * 36))  # Adjust line spacing proportionally

    def handle_event(self, event):
        global global_prefix, global_include_location, global_use_prefix
        if event.type == pygame.KEYDOWN:
            if self.editing_field == "prefix":  # Handle prefix editing
                if event.key == pygame.K_RETURN:
                    self.editing_field = None  # Stop editing
                    global_prefix = self.prefix  # Update global prefix
                elif event.key == pygame.K_BACKSPACE:
                    self.prefix = self.prefix[:-1]
                elif event.unicode and event.unicode.isprintable():
                    self.prefix += event.unicode
            elif self.editing_field == "location":  # Handle location editing
                if event.key == pygame.K_RETURN:
                    self.editing_field = None  # Stop editing
                elif event.key == pygame.K_BACKSPACE:
                    self.city = self.city[:-1]
                elif event.unicode and event.unicode.isprintable():
                    self.city += event.unicode
            elif self.editing_field == "description":  # Handle description editing
                if event.key == pygame.K_RETURN:
                    self.editing_field = None  # Stop editing
                elif event.key == pygame.K_BACKSPACE:
                    self.description = self.description[:-1]
                elif event.unicode and event.unicode.isprintable():
                    self.description += event.unicode
            else:  # Handle other events
                if event.key == pygame.K_RETURN:
                    self.done = True
                elif event.key == pygame.K_F4:  # Edit prefix
                    self.editing_field = "prefix"
                elif event.key == pygame.K_F1:  # Edit location
                    self.editing_field = "location"
                elif event.key == pygame.K_F2:  # Toggle location
                    self.include_location = not self.include_location
                    global_include_location = self.include_location  # Update global toggle
                elif event.key == pygame.K_F5:  # Toggle prefix
                    self.use_prefix = not self.use_prefix
                    global_use_prefix = self.use_prefix  # Update global toggle
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
                elif event.unicode and event.unicode.isprintable():
                    self.description += event.unicode

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
