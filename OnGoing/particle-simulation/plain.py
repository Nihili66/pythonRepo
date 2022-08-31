import pygame
from sprites import Particle
from settings import *
import random

class Plain:
    def __init__(self, clock):
        self.display_surface = pygame.display.get_surface()
        self.clock = clock
        self.constrained = False
        # particle groups
        self.G = 0.0001
        self.particles = []
        # particle initialization
        self.center = Particle((-150, -200), self, 100000, 20, "red")
        # self.create_random_particles()
        self.create_custom_particles()

    def create_random_particles(self):
        self.particles.append(self.center)
        for i in range(3):
            x = random.randint(-WIDTH // 2, WIDTH // 2)
            y = random.randint(- HEIGHT // 2, HEIGHT // 2)
            size = random.randint(20, 30)
            mass = random.randint(750, 1000)
            planet = Particle((x, y), self, mass, size, "white")
            planet.velocity.x = -0.2
            planet.velocity.y = -0.2
            self.particles.append(planet)

    def create_custom_particles(self):
        self.particles.append(self.center)
        self.center.velocity.y = 0.1
        planet = Particle((150, 200), self, 100000, 20, "blue")
        self.particles.append(planet)
        planet.velocity.y = -0.1

    def update(self):
        for particle in self.particles:
            particle.update()
            particle.draw(self.display_surface)
