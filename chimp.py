import pygame
from loaders import *
from sprites import *

# If fonts cannot be loaded, give warning
if not pygame.font:
    print("Warning, fonts disabled")

# If sounds mixer cannot be loaded, give warning
if not pygame.mixer:
    print("Warning, sound disabled")

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