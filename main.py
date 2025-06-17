import pygame
from constants import *
from player import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    # creates player at center of screen
    player = Player(SCREEN_WIDTH /2, SCREEN_HEIGHT / 2)

    # creates a forever loop that will allow to exit the game 
    # also update the screen to always show black foreground
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        player.update(dt)    

        screen.fill("black")
        player.draw(screen)
        pygame.display.flip()
        

        # Limits the framerate to 60 fps
        dt = clock.tick(60) / 1000


    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

if __name__ == "__main__":
    main()