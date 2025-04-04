import pygame
from image_viewer import ImageViewer
from renamer import rename_image

from pathlib import Path
import os
import argparse

VERSION = "0.1"

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
        while True:
            image_path = self.images[index]
            print(f"\nProcessing file {index + 1}/{len(self.images)}: {image_path.name}")

            # Pass the current file and its change entry to ImageViewer
            viewer = ImageViewer(image_path, self.changes[index])
            viewer.run()

            # Update the change entry after processing
            self.changes[index] = viewer.get_changes()

            # Handle navigation
            if not viewer.running:  # If ESC was pressed, stop processing
                break
            elif viewer.next_image:
                index = (index + 1) % len(self.images)  # Move to the next image, loop to the start if at the end
            elif viewer.previous_image:
                index = (index - 1) % len(self.images)  # Move to the previous image, loop to the end if at the start
            else:
                break  # Exit if neither flag is set

    def generate_batch_file(self, output_filename="rename_batch.bat"):
        # Generate a batch file for renaming or moving files to the "deleted" folder
        deleted_folder = self.folder / "deleted"
        batch_file_path = self.folder / output_filename  # Write the batch file into the photos folder

        with open(batch_file_path, "w") as batch_file:
            # Add a command to create the "deleted" folder (throws an error if it already exists)
            batch_file.write(f"mkdir \"{deleted_folder}\"\n")

            for change in self.changes:
                original = change["original"]
                proposed = change["proposed"]
                original_path = self.folder / original

                if change["delete"]:
                    # Move the file to the "deleted" folder
                    deleted_path = deleted_folder / original
                    batch_file.write(f"move \"{original_path}\" \"{deleted_path}\"\n")
                elif original != proposed:
                    # Rename the file
                    proposed_path = self.folder / proposed
                    batch_file.write(f"rename \"{original_path}\" \"{proposed_path}\"\n")

        print(f"Batch file saved to {batch_file_path}")

    def run(self):
        self.process_files()
        self.generate_batch_file()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Auto Image Renamer v{VERSION}: Rename images interactively based on EXIF data and user input.")
    parser.add_argument("folder", help="Path to the folder containing images to rename.")
    args = parser.parse_args()

    folder = args.folder
    app = AutoImageRenamer(folder_path=folder, test_mode=True)
    app.run()
