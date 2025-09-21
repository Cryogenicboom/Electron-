# Game settings and constants (pixels/sec units for speeds)

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Electron (pixels per second movement)
ELECTRON_SPEED = 350.0
ELECTRON_IMAGE = r"D:\projects\pygame\Electro\images_\electron.png"
ELECTRON_SIZE = (64, 64)  # resize electron image

# Obstacles (pixels per second)
OBSTACLE_BASE_SPEED = 300.0
OBSTACLE_ACCELERATION = 5.0  # speed increase per second (px/sec^2)
ATOM_SIZE = (64, 64)
WAVE_SIZE = (140, 100)

# Spawn timing
SPAWN_INTERVAL_MIN = 0.9
SPAWN_INTERVAL_MAX = 1.6

# Attraction behavior (per-atom; used to pull electron vertically when near)
# Higher number = stronger pull (pixels/sec^2 equivalent)
ATOM_ATTRACTION = {
    "hydrogen": 40.0,
    "oxygen": 60.0,
    "titanium": 120.0,
    "uranium": 200.0,
    "plutonium": 170.0,
    "gold": 150.0
}
ATOM_ATTRACTION_RANGE = 350  # horizontal distance in pixels where attraction applies

# Waves
WAVE_IMAGES = {
    "electric": r"D:\projects\pygame\Electro\images_\electricwave.png",
    "magnetic": r"D:\projects\pygame\Electro\images_\magneticwave.png"
}
MAGNETIC_SLOW_DURATION = 1.5  # seconds slow when hit
MAGNETIC_SLOW_FACTOR = 0.45   # fraction of normal speed during slow

# Atom images
ATOM_IMAGES = {
    "hydrogen": r"D:\projects\pygame\Electro\images_\hydrogen.png",
    "oxygen": r"D:\projects\pygame\Electro\images_\oxygen.png",
    "titanium": r"D:\projects\pygame\Electro\images_\titanium.png",
    "uranium": r"D:\projects\pygame\Electro\images_\uranium.png",
    "plutonium": r"D:\projects\pygame\Electro\images_\plutonium.png",
    "gold": r"D:\projects\pygame\Electro\images_\gold.png"
}

# Accelerator / intro
ACCELERATOR_IMAGE = r"D:\projects\pygame\Electro\images_\accelarator.png"
ACCELERATOR_SIZE = (220, 160)
INTRO_DURATION = 1.6  # seconds: electron comes out of accelerator