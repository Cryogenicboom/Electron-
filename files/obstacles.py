# Obstacle classes and manager for Electron Dodge Game

import pygame
import random
import math
from configurations import settings

def _load_image(path, size=None):
    surf = pygame.image.load(path)
    try:
        surf = surf.convert_alpha()
    except Exception:
        surf = surf.convert()
    if size:
        surf = pygame.transform.smoothscale(surf, size)
    if surf.get_alpha() is None:
        surf.set_colorkey((0,0,0))
    return surf

class Obstacle:
    def __init__(self, type_name, image_path, speed, y=None):
        self.type = type_name
        img = _load_image(image_path, settings.ATOM_SIZE if type_name in settings.ATOM_IMAGES else settings.WAVE_SIZE)
        self.image = img
        self.rect = self.image.get_rect()
        # spawn at right edge (small random vertical)
        self.rect.x = settings.SCREEN_WIDTH + random.randint(0, 80)
        self.rect.y = y if y is not None else random.randint(40, settings.SCREEN_HEIGHT - 40 - self.rect.height)
        self.speed = speed  # px/sec

        # wave-specific params
        self.osc_amp = 28
        self.osc_speed = random.uniform(1.2, 2.2)  # frequency
        self.spawn_time = pygame.time.get_ticks()

    def update(self, dt):
        # move left (dt in seconds)
        self.rect.x -= int(self.speed * dt)
        # electric wave vertical oscillation
        if self.type == "electric_wave":
            t = (pygame.time.get_ticks() - self.spawn_time) / 1000.0
            offset = int(self.osc_amp * math.sin(t * self.osc_speed))
            self.rect.y += offset
            # clamp to screen
            if self.rect.y < 0:
                self.rect.y = 0
            if self.rect.y + self.rect.height > settings.SCREEN_HEIGHT:
                self.rect.y = settings.SCREEN_HEIGHT - self.rect.height

    def apply_attraction(self, electron, dt):
        # Attract electron vertically if this is an atom and within horizontal range
        if self.type in settings.ATOM_IMAGES:
            dx = self.rect.centerx - electron.rect.centerx
            if 0 < dx < settings.ATOM_ATTRACTION_RANGE:
                range_frac = 1.0 - (dx / settings.ATOM_ATTRACTION_RANGE)
                force = settings.ATOM_ATTRACTION.get(self.type, 60.0) * range_frac
                dy = (self.rect.centery - electron.rect.centery)
                if dy == 0:
                    return
                dir_sign = 1 if dy > 0 else -1
                delta_y = dir_sign * min(abs(dy), force * dt)
                electron.apply_force(delta_y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def is_off_screen(self):
        return self.rect.right < 0

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.spawn_timer = random.uniform(settings.SPAWN_INTERVAL_MIN, settings.SPAWN_INTERVAL_MAX)
        self.base_speed = settings.OBSTACLE_BASE_SPEED

    def update(self, dt, game_time, intro_done):
        # increase speed over game_time
        current_speed = self.base_speed + settings.OBSTACLE_ACCELERATION * max(0.0, game_time)
        # spawn only after intro animation completes
        if intro_done:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self.spawn_obstacle(current_speed)
                self.spawn_timer = random.uniform(settings.SPAWN_INTERVAL_MIN, settings.SPAWN_INTERVAL_MAX)

        # update obstacles
        for obs in self.obstacles[:]:
            obs.speed = current_speed
            obs.update(dt)
            if obs.is_off_screen():
                self.obstacles.remove(obs)

    def spawn_obstacle(self, speed):
        types = list(settings.ATOM_IMAGES.keys()) + ["electric_wave", "magnetic_wave"]
        t = random.choice(types)

        if t in settings.ATOM_IMAGES:
            image_path = settings.ATOM_IMAGES[t]
        elif t == "electric_wave":
            image_path = settings.WAVE_IMAGES["electric"]
        else:
            image_path = settings.WAVE_IMAGES["magnetic"]

        if t == "gold":
            # spawn gold then immediate extra atom with same y
            gold_obs = Obstacle("gold", settings.ATOM_IMAGES["gold"], speed)
            self.obstacles.append(gold_obs)
            # spawn another different atom right after at same vertical position
            atom_types = [k for k in settings.ATOM_IMAGES.keys() if k != "gold"]
            extra = random.choice(atom_types)
            extra_obs = Obstacle(extra, settings.ATOM_IMAGES[extra], speed, y=gold_obs.rect.y)
            # offset x a bit to give slight separation
            extra_obs.rect.x += 40
            self.obstacles.append(extra_obs)
        else:
            obs = Obstacle(t, image_path, speed)
            self.obstacles.append(obs)

    def draw(self, screen):
        for obs in self.obstacles:
            obs.draw(screen)