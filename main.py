from image_viewer import ImageViewer
from exif_reader import get_image_date, get_gps_coordinates
from geolocator import reverse_geocode
from voice_input import record_description
from renamer import rename_image

from pathlib import Path
import time

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

        # Record voice input
        description = record_description()

        # Rename the file
        rename_image(image_path, date, city, description, test_mode=self.test_mode)

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