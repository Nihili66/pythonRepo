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
        self.center = Particle((0, 0), self, 200000, 50, "yellow")
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
        planet1 = Particle((100, 0), self, 1000, 7, "red")
        self.particles.append(planet1)
        planet1.velocity.y = 0.4
        planet = Particle((350, 0), self, 10000, 10, "blue")
        self.particles.append(planet)
        planet.velocity.y = 0.25
        moon = Particle((400, 0), self, 1, 3, "white")
        self.particles.append(moon)
        moon.velocity.y = 0.3

    def update(self):
        for particle in self.particles:
            particle.update()
            particle.draw(self.display_surface, self.center)
