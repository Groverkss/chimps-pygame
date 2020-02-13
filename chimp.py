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
            colorkey = image.get_at((0, 0))
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
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print("Cannot load sound:", name)
        raise SystemError(message)
    return sound

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

def main():

    # Dimension of the game window
    displaySize = (468, 60)

    # Fps of game
    frame_per_sec = 60

    # Initialise pygame
    pygame.init()

    # Initialise game window
    screen = pygame.display.set_mode(displaySize)
    pygame.display.set_caption("Chimps")
    # Hide mouse in game window
    pygame.mouse.set_visible(0)

    # Game background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Game background text
    if pygame.font:
        # None = default font
        font = pygame.font.Font(None, 36)
        text = font.render("Slap the Chimp", 1, (10, 10, 10))
        textpos = text.get_rect(centerx = background.get_width() / 2)
        background.blit(text, textpos)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Load sounds
    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('punch.wav')

    # Load sprites
    chimp = Chimp()
    fist = Fist()
    allsprites = pygame.sprite.RenderPlain((fist, chimp))

    # Load clock
    clock = pygame.time.Clock()

    # Main loop
    while True:
        # Run at 60fps
        clock.tick(frame_per_sec)

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play()
                    chimp.punched()
                else:
                    whiff_sound.play()
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()

        allsprites.update()

        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit

main()