from ursina import *
from sprites import Universe, Player, Planet

class Plain(Ursina):
    def __init__(self, size):
        super().__init__()
        # universe settings
        self.universe = Universe(size, 'assets/universe.jpg')
        self.dt = 0.5
        self.G = 0.0001
        # player
        self.player = Player((-200, -50, 0))
        # objects
        self.objects = []
        self.create_custom_objects()
        # self.create_random_objects()

    def create_custom_objects(self):
        sun = Planet((-125, -125, 20), 10, 50000, self, 'assets/sun.jpg')
        self.objects.append(sun)
        sun.velocity.x = 0.35
        sun.velocity.y = 0.35
        sun2 = Planet((-125, -125, -20), 10, 50000, self, 'assets/sun.jpg')
        self.objects.append(sun2)
        sun2.velocity.z = 0.35
        sun2.velocity.y = 0.35

    def create_random_objects(self):
        for i in range(50):
            x = random.randint(-200, 200)
            y = random.randint(-200, 200)
            z = random.randint(-200, 200)
            size = random.randint(1, 10)
            mass = random.randint(10000, 50000)
            self.objects.append(Planet((x, y, z), size, mass, self, tcolor="random"))
