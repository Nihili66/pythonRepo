import pygame
import math
from settings import *

class Particle:
    def __init__(self, pos, plain, mass, size):
        # particle initialization
        self.plain = plain
        self.x = pos[0]
        self.y = pos[1]
        self.initialized = False
        self.others = None
        # particle characteristics
        self.size = size
        self.mass = mass
        # particle physics
        self.velocity = pygame.math.Vector2()
        self.acceleration = pygame.math.Vector2()
        self.trajectory = []

    def draw(self, surface, center):
        center_width = WIDTH / 2
        center_height = HEIGHT / 2
        offset = pygame.math.Vector2(center_width - center.x, center_height - center.y)
        pos = pygame.math.Vector2(self.x, self.y) + offset
        pygame.draw.circle(surface, (255, 255, 255), pos, self.size)
        for trajectory in self.trajectory:
            pygame.draw.circle(surface, (255, 255, 255), trajectory + offset, 1)

    def add_trajectory(self):
        traject = pygame.math.Vector2(self.x, self.y)
        self.trajectory.append(traject)
        if len(self.trajectory) > 500:
            self.trajectory.pop(0)

    def attraction(self, others):
        force = pygame.math.Vector2()
        for other in others:
            if other == self:
                continue
            # calculate distance between particles
            dx = other.x - self.x
            dy = other.y - self.y
            # pythagoras
            distance = (dx**2 + dy**2)**0.5
            # calculate gravity force
            if distance == 0:
                pass
            else:
                gforce = (self.plain.G * other.mass) / (distance**2)
                # calculate direction of gravity force
                angle = math.atan2(dy, dx)
                # apply gravity force
                force.x += gforce * math.cos(angle)
                force.y += gforce * math.sin(angle)
        # apply gravity force to acceleration
        self.acceleration.x = force.x
        self.acceleration.y = force.y

    def accelerate(self):
        self.velocity.x += self.acceleration.x
        self.velocity.y += self.acceleration.y

    def move(self):
        self.x += self.velocity.x
        self.y += self.velocity.y

    def update(self):
        if not self.initialized:
            self.others = self.plain.particles
            self.initialized = True
        self.attraction(self.others)
        self.accelerate()
        self.move()
        self.add_trajectory()



