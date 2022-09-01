from ursina import *
from sprites import Universe, Player, Planet

class Plain(Ursina):
    def __init__(self, size):
        super().__init__()
        # universe settings
        self.universe = Universe(size, 'assets/universe.jpg')
        self.dt = 100
        self.G = 0.0001
        # player
        self.player = Player((0, 10, -12000), self)
        # objects
        self.objects = []
        # self.create_solar_system()
        self.create_custom_objects()
        # self.create_random_objects()

    def create_solar_system(self):
        sun = Planet((0, 0, 0), 10000, 100000000, self, 'assets/sun.jpg')
        self.objects.append(sun)
        mercury = Planet((-15000, 0, 0), 400, 16, self, 'assets/mercury.jpg')
        self.objects.append(mercury)
        mercury.velocity.z = 0.8
        venus = Planet((-25000, 0, 0), 900, 237, self, 'assets/venus.jpg')
        self.objects.append(venus)
        venus.velocity.z = 0.6
        earth = Planet((-35000, 0, 0), 1000, 290, self, 'assets/earth.jpg')
        self.objects.append(earth)
        earth.velocity.z = 0.5

    def create_custom_objects(self):
        earth = Planet((0, 0, 0), 1000, 290, self, 'assets/earth.jpg')
        self.objects.append(earth)

    def create_random_objects(self):
        for i in range(50):
            x = random.randint(-200, 200)
            y = random.randint(-200, 200)
            z = random.randint(-200, 200)
            size = random.randint(1, 10)
            mass = random.randint(10000, 50000)
            self.objects.append(Planet((x, y, z), size, mass, self, tcolor="random"))

