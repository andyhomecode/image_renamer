import pygame
import os
from pathlib import Path
from PIL import Image
from datetime import datetime

class ImageViewer:
    def __init__(self, folder_path):
        self.folder = Path(folder_path)
        self.images = sorted([f for f in self.folder.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
        self.index = 0
        self.screen = None
        self.running = True
        self.description = ""
        self.prefix = ""
        self.include_location = True
        self.use_prefix = True
        self.done = False

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
        font = pygame.font.SysFont(None, 12)
        text_surface = font.render(f"{img_path.name} ({self.index+1}/{len(self.images)})", True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))

        self.draw_overlay()
        pygame.display.flip()

    def draw_overlay(self):
        lines = [
            f"Description: {self.description}",
            f"Prefix: {'ON' if self.use_prefix else 'OFF'} - {self.prefix if self.use_prefix else ''}",
            f"Location: {'ON' if self.include_location else 'OFF'}",
            "[F1] Toggle Location   [F2] Toggle Prefix   [Enter] Confirm"
        ]

        font = pygame.font.SysFont(None, 28)
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (20, 40 + i * 30))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.done = True
            elif event.key == pygame.K_BACKSPACE:
                self.description = self.description[:-1]
            elif event.key == pygame.K_F1:
                self.include_location = not self.include_location
            elif event.key == pygame.K_F2:
                self.use_prefix = not self.use_prefix
            elif event.key == pygame.K_RIGHT:
                self.index = (self.index + 1) % len(self.images)
                self.show_image()
                self.done = False
                self.description = ""
            elif event.key == pygame.K_LEFT:
                self.index = (self.index - 1) % len(self.images)
                self.show_image()
                self.done = False
                self.description = ""
            elif event.unicode and event.unicode.isprintable():
                self.description += event.unicode

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
