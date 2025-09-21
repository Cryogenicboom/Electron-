# Main game loop for Electron Dodge Game

import pygame
import sys
import time

from configurations import settings
from files.electron import Electron
from files.obstacles import ObstacleManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption("Electron Dodge Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)

    # Load accelerator image and scale (fallback transparency handled in loader)
    accel_img = pygame.image.load(settings.ACCELERATOR_IMAGE)
    try:
        accel_img = accel_img.convert_alpha()
    except Exception:
        accel_img = accel_img.convert()
    accel_img = pygame.transform.smoothscale(accel_img, settings.ACCELERATOR_SIZE)
    if accel_img.get_alpha() is None:
        accel_img.set_colorkey((0,0,0))
    accel_rect = accel_img.get_rect()
    accel_rect.left = 20
    accel_rect.centery = settings.SCREEN_HEIGHT // 2

    # Create electron starting inside/behind accelerator (will animate out)
    electron = Electron(start_x=accel_rect.left - 60, start_y=accel_rect.centery - settings.ELECTRON_SIZE[1] // 2)
    target_x = 100  # final fixed X

    # obstacle manager
    obstacles = ObstacleManager()

    running = True
    start_time = time.time()
    game_time = 0.0
    intro_done = False
    intro_start = time.time()

    while running:
        dt = clock.tick(settings.FPS) / 1000.0  # seconds
        game_time = time.time() - start_time

        # --- events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        # during intro we still allow small vertical movement but no obstacle spawning
        if keys[pygame.K_UP]:
            electron.move_up(dt)
        if keys[pygame.K_DOWN]:
            electron.move_down(dt)

        # Intro animation: electron slides from accelerator to target_x over INTRO_DURATION
        if not intro_done:
            t = (time.time() - intro_start) / settings.INTRO_DURATION
            if t >= 1.0:
                t = 1.0
                intro_done = True
                electron.animating_out = False
                # fix x to target
                electron.x = target_x
                electron.rect.x = int(electron.x)
            else:
                # ease-out interpolation for nicer feel
                ease = 1 - (1 - t) * (1 - t)
                start_x = accel_rect.left - 60
                electron.x = start_x + (target_x - start_x) * ease
                electron.rect.x = int(electron.x)

        # Updates
        electron.update(dt)
        obstacles.update(dt, game_time, intro_done)

        # Attractions: obstacles influence electron (only atoms)
        for obs in list(obstacles.obstacles):
            obs.apply_attraction(electron, dt)

        # Collisions and special interactions
        for obs in list(obstacles.obstacles):
            # Only atoms are lethal
            if obs.type in settings.ATOM_IMAGES:
                if electron.rect.colliderect(obs.rect):
                    print(f"Collision with atom '{obs.type}'! Game Over.")
                    running = False
                    break
            else:
                # waves: magnetic slows (non-fatal), electric just visual/oscillation
                if obs.type == "magnetic_wave" and electron.rect.colliderect(obs.rect):
                    print("Hit magnetic wave: slowing electron.")
                    electron.apply_slow(settings.MAGNETIC_SLOW_DURATION)

        # Draw
        screen.fill(settings.WHITE)
        # draw accelerator during intro (always draw)
        screen.blit(accel_img, accel_rect.topleft)
        # draw electron
        electron.draw(screen)
        # draw obstacles
        obstacles.draw(screen)

        # draw score (only count time after intro)
        score_time = int(max(0, game_time - settings.INTRO_DURATION) if intro_done else 0)
        score_text = font.render(f"Score: {score_time}", True, settings.BLACK)
        screen.blit(score_text, (20, 20))

        pygame.display.flip()

    # Game over
    print("Game loop ended. Showing Game Over screen.")
    game_over_text = font.render("Game Over!", True, (200, 0, 0))
    screen.blit(game_over_text, (settings.SCREEN_WIDTH // 2 - 120, settings.SCREEN_HEIGHT // 2 - 30))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()