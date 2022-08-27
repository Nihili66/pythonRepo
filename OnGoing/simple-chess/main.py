import sys
import pygame
from gmanager import GManager
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('Chess Game')
        # general setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.background = pygame.Surface((WIDTH, HEIGTH))
        self.background.fill(pygame.Color('#000000'))
        self.clock = pygame.time.Clock()
        # gui setup
        self.gm = GManager()

    def run(self):
        while True:
            for event in pygame.event.get():
                # quit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # gui events and game initialization
                self.gm.manager.process_events(event)
                self.gm.game_init(event)
                # game events
                self.gm.game_play(event)

            self.gm.update(self.clock.tick(FPS), self.screen)
            pygame.display.update()
            self.screen.blit(self.background, (0, 0))


if __name__ == '__main__':
    game = Game()
    game.run()
