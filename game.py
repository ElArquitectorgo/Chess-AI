import pygame

class Game:
    def __init__(self, WIDTH: int, HEIGHT: int, TITLE: str, TICK: int):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.tick = TICK

    def run(self):
        while True:
            self.clock.tick(self.tick)
            self.events()
            self.draw()