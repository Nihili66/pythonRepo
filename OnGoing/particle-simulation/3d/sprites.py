from ursina import *

class Universe(Entity):
    def __init__(self, size, textu):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=textu,
            scale=size,
            double_sided=True)


class Player(Entity):
    def __init__(self, position):
        super().__init__()
        # camera settings
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.pink, scale=.008, rotation_z=45)
        self.height = 2
        self.camera_pivot = Entity(parent=self, y=self.height)
        camera.parent = self.camera_pivot
        camera.position = (0, 0, 0)
        camera.rotation = (0, 0, 0)
        camera.fov = 90
        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)

        # physics settings
        self.speed = 50
        self.position = position

    def update(self):
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x = clamp(self.camera_pivot.rotation_x, -90, 90)

        self.direction = Vec3(
            self.forward * (held_keys['z'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['q']) +
            self.up * (held_keys['space'] - held_keys['left control'])
        ).normalized()

        move_amount = self.direction * time.dt * self.speed

        self.position += move_amount

    def input(self, key):
        if key == 'escape':
            if mouse.locked:
                mouse.locked = False
                self.cursor.enabled = False
            else:
                mouse.locked = True
                self.cursor.enabled = True


class Planet(Entity):
    def __init__(self, position, size, mass, universe, textu=None, tcolor=None):
        super().__init__(
            parent=scene,
            model='sphere',
            position=position,
        )

        if tcolor == "random":
            self.color = color.random_color()
        elif tcolor:
            self.color = tcolor
        if textu:
            self.texture = textu
        self.universe = universe
        self.others = self.universe.objects
        # charachteristics
        self.scale = size
        self.mass = mass
        self.collider = "sphere"
        # physics
        self.velocity = Vec3(0, 0, 0)
        self.acceleration = Vec3(0, 0, 0)

    def gravity(self):
        force = Vec3(0, 0, 0)
        for planet in self.others:
            if planet == self:
                continue
            if self.intersects(planet):
                # self.merge(planet)
                pass
            dist = (planet.position - self.position)**2
            # get distance from vector3 to scalar
            dist = dist.x + dist.y + dist.z
            force += (planet.position - self.position) * planet.mass * self.mass * self.universe.G / dist ** (3 / 2)

        self.acceleration = force

    def acceleration_update(self):
        if self.mass > 0:
            self.velocity += self.universe.dt * self.acceleration / self.mass
            self.position += self.velocity * self.universe.dt

    def merge(self, other):
        if self.mass > other.mass:
            self.scale += other.scale
            self.mass += other.mass
            self.universe.objects.remove(other)
            scene.entities.remove(other)
            other.mass = 0
            other.scale = 0
        else:
            other.scale += self.scale
            other.mass += self.mass
            self.universe.objects.remove(self)
            scene.entities.remove(self)
            self.mass = 0
            self.scale = 0

    def update(self):
        if self.mass > 0:
            self.gravity()
            self.acceleration_update()
