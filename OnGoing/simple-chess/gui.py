import pygame
import pygame_gui
from settings import *


class Welcomegui:
    def __init__(self):
        self.manager = pygame_gui.UIManager((WIDTH, HEIGTH))
        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH / 2 - 60, HEIGTH / 2 - 25), (120, 50)),
                                                         text='Start Game',
                                                         manager=self.manager)

