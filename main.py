import pygame  # Add this import
from image_viewer import ImageViewer
from exif_reader import get_image_date, get_gps_coordinates
from geolocator import reverse_geocode
from renamer import rename_image

from pathlib import Path
from datetime import datetime

class AutoImageRenamer(ImageViewer):
    def __init__(self, folder_path, test_mode=False):
        super().__init__(folder_path)
        self.test_mode = test_mode

    def handle_current_image(self):
        image_path = self.get_current_image_path()
        print(f"\nProcessing: {image_path.name}")

        # Get date
        date = get_image_date(image_path)

        # Get city from GPS if available
        gps = get_gps_coordinates(image_path)
        city = reverse_geocode(*gps) if gps else ""

        # Wait for user input via overlay
        print("Provide input using the overlay...")
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                self.handle_event(event)

            self.show_image()

        # Construct final description
        parts = []
        if self.use_prefix and self.prefix:
            parts.append(self.prefix)
        if self.description:
            parts.append(self.description)
        full_description = " ".join(parts)

        # Location toggle
        used_city = city if self.include_location else ""

        # Rename
        rename_image(image_path, date, used_city, full_description, test_mode=self.test_mode)

        # Reset for the next image
        self.done = False
        self.description = ""

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.show_image()

        # Trigger processing for the first image
        self.handle_current_image()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_event(event)

        pygame.quit()

if __name__ == "__main__":
    folder = "./photos"  # Change this to your image folder
    app = AutoImageRenamer(folder_path=folder, test_mode=True)
    app.run()
