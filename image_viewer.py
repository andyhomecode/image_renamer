import pygame
import os
from pathlib import Path
from PIL import Image

class ImageViewer:
    def __init__(self, folder_path):
        self.folder = Path(folder_path)
        self.images = sorted([f for f in self.folder.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
        self.index = 0
        self.screen = None
        self.running = True

    def show_image(self):
        img_path = self.images[self.index]
        pil_image = Image.open(img_path)
        pil_image = pil_image.convert('RGB')
        image = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)
        image = pygame.transform.scale(image, self.screen.get_size())
        self.screen.blit(image, (0, 0))
        pygame.display.set_caption(f"{img_path.name} ({self.index+1}/{len(self.images)})")
        pygame.display.flip()

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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.index = (self.index + 1) % len(self.images)
                        self.show_image()
                    elif event.key == pygame.K_LEFT:
                        self.index = (self.index - 1) % len(self.images)
                        self.show_image()

        pygame.quit()

if __name__ == "__main__":
    viewer = ImageViewer("./photos")  # Change this to your image folder
    viewer.run()
