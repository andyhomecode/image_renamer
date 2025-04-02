import pygame

class OverlayInput:
    def __init__(self, screen, date, city, prefix=""):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 28)
        self.description = ""
        self.prefix = prefix
        self.city = city
        self.date = date.strftime("%Y-%m-%d")
        self.include_location = True
        self.use_prefix = True
        self.done = False

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
            elif event.unicode and event.unicode.isprintable():
                self.description += event.unicode

    def draw(self):
        self.screen.fill((0, 0, 0))

        lines = [
            f"Date: {self.date}",
            f"Location: {'ON' if self.include_location else 'OFF'} - {self.city if self.include_location else ''}",
            f"Prefix: {'ON' if self.use_prefix else 'OFF'} - {self.prefix if self.use_prefix else ''}",
            f"Description: {self.description}",
            "[F1] Toggle Location   [F2] Toggle Prefix   [Enter] Confirm"
        ]

        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (20, 40 + i * 30))

        pygame.display.flip()

    def get_result(self):
        return {
            "description": self.description.strip(),
            "prefix": self.prefix.strip(),
            "include_location": self.include_location,
            "use_prefix": self.use_prefix
        }

    def run(self):
        clock = pygame.time.Clock()
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                self.handle_event(event)

            self.draw()
            clock.tick(30)

        return self.get_result()

# For testing standalone
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 300))
    overlay = OverlayInput(screen, date="2023-10-01", city="Tokyo", prefix="Festival")
    result = overlay.run()
    print("Overlay result:", result)
    pygame.quit()
