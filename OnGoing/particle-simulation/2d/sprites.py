import pygame
import math
from settings import *

class Particle:
    def __init__(self, pos, plain, mass, size, color):
        # particle initialization
        self.plain = plain
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.rect = pygame.draw.circle(plain.display_surface, color, pos, size)
        self.particles = None
        # particle characteristics
        self.size = size
        self.mass = mass
        # particle physics
        self.velocity = pygame.math.Vector2()
        self.acceleration = pygame.math.Vector2()
        self.trajectory = []

    def draw(self, surface, center=pygame.math.Vector2(0, 0)):
        # offsets
        center_width = WIDTH / 2
        center_height = HEIGHT / 2
        offset = pygame.math.Vector2(center_width - center.x, center_height - center.y)
        pos = pygame.math.Vector2(self.x, self.y) + offset
        # draw particle
        self.rect = pygame.draw.circle(surface, self.color, pos, self.size)
        # draw trajectory
        for trajectory in self.trajectory:
            pygame.draw.circle(surface, self.color, trajectory + offset, 1)

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
        if self.plain.constrained:
            if self.x > WIDTH // 2:
                self.velocity.x *= -1
            if self.x < -WIDTH // 2:
                self.velocity.x *= -1
            if self.y > HEIGHT // 2:
                self.velocity.y *= -1
            if self.y < -HEIGHT // 2:
                self.velocity.y *= -1

    def merge(self, other):
        self.particles.remove(other)
        self.mass += other.mass
        self.size += other.size

    def update(self):
        self.particles = self.plain.particles
        self.attraction(self.particles)
        self.accelerate()
        self.move()
        self.add_trajectory()



