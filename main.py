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
    font = pygame.font.Font(None, 36)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    lives = 3
    respawning = False
    respawn_timer = 0
    invulnerable = False
    invulnerable_timer = 0

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
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        # checks time in order to determine respawn timer, as well as invuln timer
        current_time = pygame.time.get_ticks()
        if respawning and current_time > respawn_timer:
            respawning = False
        if invulnerable and current_time > invulnerable_timer:
            invulnerable = False
            
        # checks collision and handles lives/respawning/invulnerability   
        if respawning:
        # Update everything except the player
            for obj in updatable:
                if obj != player:
                    obj.update(dt)
        else:
            # Update everything normally
            updatable.update(dt)
            for asteroid in asteroids:
                if not invulnerable and not respawning and asteroid.detect_collision(player):
                    lives -= 1 #removes a life when hit
                    print(f"Hit! Lives remaining: {lives}")
            
                    if lives > 0:
                        # Start respawn sequence
                        respawning = True
                        respawn_timer = pygame.time.get_ticks() + 2000  # 2 second delay
                
                        # Reset player position to center
                        player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        player.velocity = pygame.Vector2(0, 0)  # Stop player movement
                            
                        # Make player invulnerable
                        invulnerable = True
                        invulnerable_timer = pygame.time.get_ticks() + 3000  # 3 seconds
                            
                    else:
                        print("Game over!")
                        sys.exit()
        
                    break  # Exit the loop since we found a collision

        for roid in asteroids:
            for shot in shots:
                if roid.detect_collision(shot):
                    roid.split()
                    shot.kill()
                    score += 1

        screen.fill("black")

        # adds score counter to top left corner
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))  # Position in top-left corner

        # Add lives counter to bottom-left corner
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, SCREEN_HEIGHT - 40))  # Position in bottom-left corner

        for obj in drawable:
            if obj == player and respawning:
                continue # doesn't show player during respawn
            obj.draw(screen)
        pygame.display.flip()
        

        # Limits the framerate to 60 fps
        dt = clock.tick(60) / 1000

        


    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

if __name__ == "__main__":
    main()