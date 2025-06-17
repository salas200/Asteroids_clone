import pygame
from constants import *
from circleshape import *
from shot import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.radius = PLAYER_RADIUS
        self.rotation = 0
        self.clock = 0


    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_RIGHT]:
            self.rotate(dt * -1)
        if keys[pygame.K_d] or keys[pygame.K_LEFT]:
            self.rotate(dt)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(dt * -1)

        if keys[pygame.K_SPACE]:
            self.shoot()
        self.clock -= dt
        self.clock = max(0, self.clock)

        # Wrap around screen edges
        if self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        elif self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        
        if self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
        elif self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.clock > 0:
            return
        else:
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = pygame.Vector2(0, 1)
            shot.velocity = shot.velocity.rotate(self.rotation)
            shot.velocity = shot.velocity * PLAYER_SHOOT_SPEED
            self.clock = PLAYER_SHOOT_COOLDOWN

    def point_in_triangle(self, point):
        """Check if a point is inside the triangle using barycentric coordinates"""
        triangle_points = self.triangle()
        v0 = triangle_points[2] - triangle_points[0]  # c - a
        v1 = triangle_points[1] - triangle_points[0]  # b - a  
        v2 = point - triangle_points[0]               # point - a

        dot00 = v0.dot(v0)
        dot01 = v0.dot(v1)
        dot02 = v0.dot(v2)
        dot11 = v1.dot(v1)
        dot12 = v1.dot(v2)

        inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom

        return (u >= 0) and (v >= 0) and (u + v <= 1)

    def collides_with_circle(self, circle_center, circle_radius):
        """Check collision between triangle and circle"""
        # Check if circle center is inside triangle
        if self.point_in_triangle(circle_center):
            return True
        
        # Check distance from circle center to each triangle edge
        triangle_points = self.triangle()
        
        for i in range(3):
            edge_start = triangle_points[i]
            edge_end = triangle_points[(i + 1) % 3]
            
            # Find closest point on edge to circle center
            edge_vec = edge_end - edge_start
            to_circle = circle_center - edge_start
            
            if edge_vec.length_squared() == 0:
                closest_point = edge_start
            else:
                t = max(0, min(1, to_circle.dot(edge_vec) / edge_vec.length_squared()))
                closest_point = edge_start + t * edge_vec
            
            # Check if circle overlaps with this closest point
            if closest_point.distance_to(circle_center) <= circle_radius:
                return True
        
        return False

    # Override the collision method from CircleShape
    def detect_collision(self, other):
        """Override to use triangular collision detection"""
        if hasattr(other, 'position') and hasattr(other, 'radius'):
            return self.collides_with_circle(other.position, other.radius)
        return False





    
