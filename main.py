import pygame
from image_viewer import ImageViewer
from exif_reader import get_image_date, get_gps_coordinates
from geolocator import reverse_geocode
from renamer import rename_image, build_new_filename  # Import build_new_filename

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
        self.date = get_image_date(image_path)

        # Get city from GPS if available
        gps = get_gps_coordinates(image_path)
        self.city = reverse_geocode(*gps) if gps else ""  # Update city for overlay

        # Wait for user input via overlay
        print("Provide input using the overlay...")
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                self.handle_event(event)

            self.show_image()

        # Construct final name using build_new_filename
        full_description = f"{self.prefix} {self.description}".strip()
        final_name = build_new_filename(
            self.date,
            self.city if self.include_location else "",
            full_description,
            image_path.suffix.lower()
        )

        # TODO: Update the EXIF metadata with the edited date or other fields (e.g., location, description)

        # Rename
        rename_image(image_path, self.date, self.city if self.include_location else "", full_description, test_mode=self.test_mode)

        print(f"Final Name: {final_name}")

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
