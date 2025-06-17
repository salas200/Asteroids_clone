from circleshape import *
import random
import math
from constants import *


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.shape_points = self._generate_lumpy_shape()

    def _generate_lumpy_shape(self):
        points = []
        num_points = random.randint(8, 16) #chooses points from range

        for i in range(num_points):
            angle = (2 * math.pi * i) / num_points
            distance = self.radius * random.uniform(0.7, 1.3)

            point_x = distance * math.cos(angle)
            point_y = distance * math.sin(angle)
            points.append((point_x, point_y))

        return points
    

    def draw(self, screen):

        # Translate the shape points to the asteroid's current position
        world_points = [(self.position.x + px, self.position.y + py) for px, py in self.shape_points]
        pygame.draw.polygon(screen, "light blue", world_points, 2)

    def update(self, dt):
        self.position += self.velocity * dt

        # Wrap around screen edges
        if self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        elif self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        
        if self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
        elif self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius

    # this will split up the asteroids into smaller ones when shot,
    # the smallest asteroid will just be deleted
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        old_radius = self.radius
        new_radius = old_radius - ASTEROID_MIN_RADIUS
        angle = random.uniform(20, 50)
        new_velocity1 = self.velocity.rotate(angle)
        new_velocity2 = self.velocity.rotate(-angle)

        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid1.velocity= new_velocity1 * 1.2
        
        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid2.velocity = new_velocity2 * 1.2


