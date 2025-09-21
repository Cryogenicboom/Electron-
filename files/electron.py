# files/electron.py
import pygame
from configurations import settings

def _load_image(path, size=None):
    surf = pygame.image.load(path)
    try:
        surf = surf.convert_alpha()
    except Exception:
        surf = surf.convert()
    if size:
        surf = pygame.transform.smoothscale(surf, size)
    # If image has no alpha, treat pure black as transparent fallback
    if surf.get_alpha() is None:
        surf.set_colorkey((0, 0, 0))
    return surf

class Electron:
    def __init__(self, start_x=None, start_y=None):
        # Load and scale image
        self.image = _load_image(settings.ELECTRON_IMAGE, settings.ELECTRON_SIZE)
        # Position (x may be animated during intro)
        self.x = settings.SCREEN_WIDTH + 200 if start_x is None else start_x
        self.y = settings.SCREEN_HEIGHT // 2 if start_y is None else start_y
        self.speed = settings.ELECTRON_SPEED
        self.rect = self.image.get_rect(topleft=(int(self.x), int(self.y)))
        # slow effect
        self.slow_timer = 0.0
        self.slow_factor = 1.0
        # playing intro animation flag
        self.animating_out = True

    def move_up(self, dt):
        # dt-based movement
        self.y -= self.speed * self.slow_factor * dt
        if self.y < 0:
            self.y = 0
        self.rect.y = int(self.y)

    def move_down(self, dt):
        self.y += self.speed * self.slow_factor * dt
        bottom = settings.SCREEN_HEIGHT - self.rect.height
        if self.y > bottom:
            self.y = bottom
        self.rect.y = int(self.y)

    def apply_slow(self, duration):
        # apply magnetic slow (non-stacking)
        self.slow_timer = max(self.slow_timer, duration)
        self.slow_factor = settings.MAGNETIC_SLOW_FACTOR

    def apply_force(self, delta_y):
        # immediate small displacement caused by attraction (keeps control responsive)
        self.y += delta_y
        # clamp
        if self.y < 0:
            self.y = 0
        if self.y + self.rect.height > settings.SCREEN_HEIGHT:
            self.y = settings.SCREEN_HEIGHT - self.rect.height
        self.rect.y = int(self.y)

    def update(self, dt):
        # update slow effect timer
        if self.slow_timer > 0:
            self.slow_timer -= dt
            if self.slow_timer <= 0:
                self.slow_timer = 0
                self.slow_factor = 1.0
        # update rect x/y (x might change during intro)
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))
