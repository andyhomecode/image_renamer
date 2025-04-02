from image_viewer import ImageViewer
from exif_reader import get_image_date, get_gps_coordinates
from geolocator import reverse_geocode
from voice_input import record_description
from renamer import rename_image
from ui_overlay import OverlayInput


from pathlib import Path
import time
from datetime import datetime

class AutoImageRenamer(ImageViewer):
    def __init__(self, folder_path, test_mode=False):
        super().__init__(folder_path)
        self.test_mode = test_mode
        self.prefix = ""
        self.use_prefix = True
        self.include_location = True


    def handle_current_image(self):
        image_path = self.get_current_image_path()
        print(f"\nProcessing: {image_path.name}")

        # Get date
        date = get_image_date(image_path)

        # Get city from GPS if available
        gps = get_gps_coordinates(image_path)
        city = reverse_geocode(*gps) if gps else ""

        # Record voice input
        # description = record_description()

        # Use Overlay UI for input
        overlay = OverlayInput(self.screen, date, city, prefix=self.prefix)
        result = overlay.run()

        # Update toggles and persistent prefix
        self.include_location = result["include_location"]
        self.use_prefix = result["use_prefix"]
        if self.use_prefix:
            self.prefix = result["prefix"]
    
        # Construct final description
        parts = []
        if self.use_prefix and self.prefix:
            parts.append(self.prefix)
        if result["description"]:
            parts.append(result["description"])
        full_description = " ".join(parts)
    
        # Location toggle
        used_city = city if self.include_location else ""
    
        # Rename
        rename_image(image_path, date, used_city, full_description, test_mode=self.test_mode)

    def run(self):
        import pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.show_image()

        # Trigger processing for the first image
        self.handle_current_image()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.index = (self.index + 1) % len(self.images)
                        self.show_image()
                        self.handle_current_image()
                    elif event.key == pygame.K_LEFT:
                        self.index = (self.index - 1) % len(self.images)
                        self.show_image()
                        self.handle_current_image()

        pygame.quit()

if __name__ == "__main__":
    folder = "./photos"  # Change this to your image folder
    app = AutoImageRenamer(folder_path=folder, test_mode=True)
    app.run()
