import os
import sys
import pygame

from pygame.locals import *

# If fonts cannot be loaded, give warning
if not pygame.font:
    print("Warning, fonts disabled")

# If sounds mixer cannot be loaded, give warning
if not pygame.mixer:
    print("Warning, sound disabled")

# Load image and throw error if image cannot be loaded
def load_image(name, colorkey = None):

    # Loads image located at ./data/name
    fullname = os.path.join("data", name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Cannot load image:", name)
        raise SystemExit(message)
    image = image.convert()

    # Sets colorkey
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at(0, 0)
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

# Load sound and throw error if sound cannot be loaded
def load_sound(name):

    # If sound mixer not loaded then don't load sound
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()

    # Loads image located at ./data/name
    fullname = os.path.join("data", name)
    try:
        sound = pygame.mixer.load(fullname)
    except pygame.error as message:
        print("Cannot load sound:", name)
        raise SystemError(message)
    return sound