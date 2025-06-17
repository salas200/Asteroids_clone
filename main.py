import pygame
import sys
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from circleshape import *
from shot import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    # creates objects into groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # containers for groups
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable,)
    Player.containers = (updatable, drawable)
    Shot.containers = (updatable, drawable, shots)

    # places player into center screen and places asteroids
    player = Player(SCREEN_WIDTH /2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    # creates a forever loop that will allow to exit the game
    # detects collision of player and asteroid, will result in game over
    # detects collision of bullet and asteroid, will kill both if True 
    # also update the screen to always show black foreground
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.detect_collision(player):
                print("Game over!")
                sys.exit()

        for obj in asteroids:
            for obj2 in shots:
                if obj.detect_collision(obj2):
                    obj.kill()
                    obj2.kill()

        screen.fill("black")
        for obj in drawable:
            obj.draw(screen)
        pygame.display.flip()
        

        # Limits the framerate to 60 fps
        dt = clock.tick(60) / 1000


    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

if __name__ == "__main__":
    main()