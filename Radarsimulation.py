import pygame
import math
import random
import os


pygame.init()

#audio
pygame.mixer.init()
base_dir = os.path.dirname(os.path.abspath(__file__))
ping = pygame.mixer.Sound(os.path.join(base_dir, "Audio", "ping.mp3"))
radar = pygame.mixer.Sound(os.path.join(base_dir, "Audio", "radar.mp3"))

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Radar Simulation")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)


clock = pygame.time.Clock()

# Radar settings
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 250
RADIUS2 = 200
RADIUS3 = 150
RADIUS4 = 100
RADIUS5 = 50
ANGLE_STEP = 0.5  # Rotation speed of the radar in degrees

# Object class to manage fading
class RadarObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alpha = 255  
        self.scanned = False 

    def fade(self):
        if not self.scanned:  
            self.alpha = max(self.alpha - 5, 0)  
        else:
            self.alpha = 255  # Reset to full opacity when scanned
        return (self.x, self.y, self.alpha)

    def reset(self):
        self.scanned = False
        self.alpha = 255  # Reset to fully visible


# Detected objects (randomly placed for simulation)
objects = [
    RadarObject(random.randint(CENTER[0] - RADIUS, CENTER[0] + RADIUS), 
                random.randint(CENTER[1] - RADIUS, CENTER[1] + RADIUS))
    for _ in range(10)
]

# Filter objects within the radar radius
objects = [obj for obj in objects if math.hypot(obj.x - CENTER[0], obj.y - CENTER[1]) <= RADIUS]

# Transparent surface for fading effect
fade_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
fade_surface.fill((0, 0, 0, 10))  # 10 is the alpha value for transparency

def check_if_in_radar_beam(obj, angle):
    # Check if the object is within the radar beam range
    obj_angle = math.degrees(math.atan2(CENTER[1] - obj.y, obj.x - CENTER[0])) % 360
    return abs(obj_angle - angle) <= 5  # +/- 5 degrees tolerance for radar beam width

def draw_radar(angle):
    # Apply fading effect
    screen.blit(fade_surface, (0, 0))

    # Draw radar circle
    pygame.draw.circle(screen, DARK_GREEN, CENTER, RADIUS, 1)
    pygame.draw.circle(screen, DARK_GREEN, CENTER, RADIUS2, 1)
    pygame.draw.circle(screen, DARK_GREEN, CENTER, RADIUS3, 1)
    pygame.draw.circle(screen, DARK_GREEN, CENTER, RADIUS4, 1)
    pygame.draw.circle(screen, DARK_GREEN, CENTER, RADIUS5, 1)

    # Draw crosshairs
    pygame.draw.line(screen, DARK_GREEN, (CENTER[0] - RADIUS, CENTER[1]), (CENTER[0] + RADIUS, CENTER[1]), 1)
    pygame.draw.line(screen, DARK_GREEN, (CENTER[0], CENTER[1] - RADIUS), (CENTER[0], CENTER[1] + RADIUS), 1)

    # Draw detected objects
    for obj in objects:
        # Check if the object is in the radar beam
        if check_if_in_radar_beam(obj, angle):
            if not obj.scanned: 
                obj.scanned = True
                ping.set_volume(0.3)
                ping.play()  # Play sound when scanned
        else:
            obj.scanned = False

        # Draw object with fading effect
        obj_x, obj_y, alpha = obj.fade()
        faded_surface = pygame.Surface((10, 10), pygame.SRCALPHA)
        faded_surface.fill((GREEN[0], GREEN[1], GREEN[2], alpha))
        screen.blit(faded_surface, (obj_x - 5, obj_y - 5))
        
    # Calculate radar line endpoints
    end_x = CENTER[0] + RADIUS * math.cos(math.radians(angle))
    end_y = CENTER[1] - RADIUS * math.sin(math.radians(angle))

    # Draw radar beam
    beam_points = [
        CENTER,
        (CENTER[0] + RADIUS * math.cos(math.radians(angle - 2)), CENTER[1] - RADIUS * math.sin(math.radians(angle - 2))),
        (CENTER[0] + RADIUS * math.cos(math.radians(angle + 2)), CENTER[1] - RADIUS * math.sin(math.radians(angle + 2)))
    ]
    pygame.draw.polygon(screen, GREEN + (100,), beam_points)  # Alpha value for transparency

# Main loop
running = True
angle = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the radar
    draw_radar(angle)

    # Update the display
    pygame.display.flip()

    #Play radar sound
   # radar.set_volume(0.1)
   # radar.play()
    
    # Increment the angle
    angle = (angle + ANGLE_STEP) % 360

    # Control the frame rate
    clock.tick(60)

pygame.quit()