import pygame
from sprites import Particle
from settings import *
import random

class Plain:
    def __init__(self, clock):
        self.display_surface = pygame.display.get_surface()
        self.clock = clock
        # particle groups
        self.G = 0.0001
        self.particles = []
        # particle initialization
        self.center = Particle((0, 0), self, 100000, 50)
        # self.create_random_particles()
        self.create_custom_particles()

    def create_random_particles(self):
        self.particles.append(self.center)
        self.center.velocity.x = -0.5
        self.center.velocity.y = -0.5
        for i in range(2):
            x = 150 * (i + 1)
            y = 0
            size = random.randint(10, 15)
            mass = random.randint(5000, 7500)
            planet = Particle((x, y), self, mass, size)
            planet.velocity.y = -1
            self.particles.append(planet)

    def create_custom_particles(self):
        self.particles.append(self.center)
        self.center.velocity.x = -0.1
        self.center.velocity.y = -0.1
        planet = Particle((200, 0), self, 1, 10)
        self.particles.append(planet)
        planet.velocity.y = -0.2

    def update(self):
        for particle in self.particles:
            particle.update()
            particle.draw(self.display_surface, self.center)
