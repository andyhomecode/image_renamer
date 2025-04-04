import pygame
from image_viewer import ImageViewer
from renamer import rename_image

from pathlib import Path

class AutoImageRenamer:
    def __init__(self, folder_path, test_mode=False):
        self.folder = Path(folder_path)
        self.test_mode = test_mode
        self.changes = []  # List to track changes (original name, proposed new name, delete flag)

        # Build the list of files and initialize changes
        self.images = sorted([f for f in self.folder.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
        for img in self.images:
            self.changes.append({"original": img.name, "proposed": img.name, "delete": False, "description": ""})

    def process_files(self):
        index = 0  # Start with the first image
        while 0 <= index < len(self.images):
            image_path = self.images[index]
            print(f"\nProcessing file {index + 1}/{len(self.images)}: {image_path.name}")

            # Pass the current file and its change entry to ImageViewer
            viewer = ImageViewer(image_path, self.changes[index])
            viewer.run()

            # Update the change entry after processing
            self.changes[index] = viewer.get_changes()

            # Handle navigation
            if viewer.next_image:
                index += 1  # Move to the next image
            elif viewer.previous_image:
                index -= 1  # Move to the previous image
            else:
                break  # Exit if neither flag is set

    def generate_batch_file(self, output_path="rename_batch.bat"):
        # Generate a batch file for renaming or deleting files
        with open(output_path, "w") as batch_file:
            for change in self.changes:
                original = change["original"]
                proposed = change["proposed"]
                if change["delete"]:
                    batch_file.write(f"del \"{original}\"\n")
                elif original != proposed:
                    batch_file.write(f"rename \"{original}\" \"{proposed}\"\n")
        print(f"Batch file saved to {output_path}")

    def run(self):
        self.process_files()
        self.generate_batch_file()

if __name__ == "__main__":
    folder = "./photos"  # Change this to your image folder
    app = AutoImageRenamer(folder_path=folder, test_mode=True)
    app.run()
