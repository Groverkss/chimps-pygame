import pygame
from loaders import *

# Fist which follows the mouse
class Fist(pygame.sprite.Sprite):

    # Initialising Fist
    def __init__(self):
        # Call sprite initialiser
        pygame.sprite.Sprite.__init__(self)
        
        # Initialise image and collision state
        self.image, self.rect = load_image('fist.bmp', -1)
        self.punching = 0

    # Move fist based on mouse pointer position
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    # Returns Trueif fist collides with the target
    def punch(self, target):
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, 5)
            return hitbox.colliderect(target.rect)

    # Pulls the punch back
    def unpunch(self):
        self.punching = 0

# Chimp critter which moves across the screen
class Chimp(pygame.sprite.Sprite):

    # Initialising Chimp
    def __init__(self):
        # Call sprite initialiser
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = load_image('chimp.bmp', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (10, 10)
        self.move = 9
        self.dizzy = 0

    # Walks or spins the monkey depending on collision state
    def update(self):
        if self.dizzy:
            self._spin()
        else:
            self._walk()
    
    # Move monekey across the screen and turn at edges
    def _walk(self):
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.rect = newpos

    # Spin the monkey
    def _spin(self):
        center = self.rect.center
        self.dizzy += 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center = center)

    # Will cause monkey to start spinning
    def punched(self):
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image