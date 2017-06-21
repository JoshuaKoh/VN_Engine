import pygame
from time import sleep
import my_lib
from my_lib import *

inTransition = False # Is the user viewing a transition?
transitionBg = None # What is the user view while in a transition?


# TRANSITIONS
# fadeto colors: black, white, red
def transition_fadeto(screen, clock, fadeColor = "BLACK"):
    global transitionBg
    fadeColor = fadeColor.upper()
    color = None
    if fadeColor == "BLACK":
        color = [0, 0, 0, 0]
        transitionBg = (0, 0, 0)
    elif fadeColor == "RED":
        color = [255, 0, 0, 0]
        transitionBg = (255, 0, 0)
    elif fadeColor == "WHITE":
        color = [255, 255, 255, 0]
        transitionBg = (255, 255, 255)
    else:
        # In the case the transition is broken, inTransition needs to be turned off again
        global inTransition
        inTransition = False
        return

    for i in range(8):
        # Prep fade color
        color[3] = (32 * (i + 1)) - 1
        textbox = pygame.Surface((o.WIDTH, o.HEIGHT), pygame.SRCALPHA)
        textbox.fill(color)

        # Prep text box
        textbox = pygame.Surface((o.WIDTH, o.HEIGHT//2 - (o.HEIGHT//2)//6 - TEXT_BOX_GUTTER), pygame.SRCALPHA)
        textbox.fill(C_TEXT_BOX)

        # Blit all 3
        screen.blit(get_image(o.currentBgPath), (0, 0))
        screen.blit(textbox, (0, o.HEIGHT//2 + (o.HEIGHT//2)//6))
        screen.blit(textbox, (0, 0))

        pygame.display.flip()
        clock.tick(o.FPS)
        sleep(0.1) # Make transition slower

# fadefrom colors: black, white, red
def transition_fadefrom(screen, clock, fadeColor = "BLACK"):
    global transitionBg
    fadeColor = fadeColor.upper()
    color = None
    if fadeColor == "BLACK":
        color = [0, 0, 0, 0]
        transitionBg = (0, 0, 0)
    elif fadeColor == "RED":
        color = [255, 0, 0, 0]
        transitionBg = (255, 0, 0)
    elif fadeColor == "WHITE":
        color = [255, 255, 255, 0]
        transitionBg = (255, 255, 255)
    else:
        return

    for i in range(8):
        # Prep fade color
        color[3] = 256 - ((32 * (i + 1)) - 1)
        textbox = pygame.Surface((o.WIDTH, o.HEIGHT), pygame.SRCALPHA)
        textbox.fill(color)

        # Prep text box
        textbox = pygame.Surface((o.WIDTH, o.HEIGHT//2 - (o.HEIGHT//2)//6 - TEXT_BOX_GUTTER), pygame.SRCALPHA)
        textbox.fill(C_TEXT_BOX)

        # Blit all 3
        screen.blit(get_image(o.currentBgPath), (0, 0))
        screen.blit(textbox, (0, o.HEIGHT//2 + (o.HEIGHT//2)//6))
        screen.blit(textbox, (0, 0))

        pygame.display.flip()
        clock.tick(o.FPS)
        sleep(0.1) # Make transition slower

# fadefrom colors: black, white, red
def transition_fadetoandfrom(screen, clock, fadeColor = "BLACK", timeInColor = 0.1):
    global transitionBg
    fadeColor = fadeColor.upper()
    color = None

    if fadeColor == "BLACK":
        color = [0, 0, 0, 0]
        transitionBg = (0, 0, 0)
    elif fadeColor == "RED":
        color = [255, 0, 0, 0]
        transitionBg = (255, 0, 0)
    elif fadeColor == "WHITE":
        color = [255, 255, 255, 0]
        transitionBg = (255, 255, 255)
    else:
        return

    # Fade out!
    for i in range(8):
        # Prep fade color
        color[3] = (32 * (i + 1)) - 1
        textbox = pygame.Surface((o.WIDTH, o.HEIGHT), pygame.SRCALPHA)
        textbox.fill(color)

        # Prep text box
        textbox = pygame.Surface((o.WIDTH, o.HEIGHT//2 - (o.HEIGHT//2)//6 - TEXT_BOX_GUTTER), pygame.SRCALPHA)
        textbox.fill(C_TEXT_BOX)

        # Blit all 3
        screen.blit(get_image(o.currentBgPath), (0, 0))
        screen.blit(textbox, (0, o.HEIGHT//2 + (o.HEIGHT//2)//6))
        screen.blit(textbox, (0, 0))

        pygame.display.flip()
        clock.tick(o.FPS)
        sleep(0.1) # Make transition slower

    # Wait for some time in color
    sleep(float(timeInColor))

    # Fade in!
    for i in range(8):
        # Prep fade color
        color[3] = 256 - ((32 * (i + 1)) - 1)
        textbox = pygame.Surface((o.WIDTH, o.HEIGHT), pygame.SRCALPHA)
        textbox.fill(color)

        # Prep text box
        textbox = pygame.Surface((o.WIDTH, o.HEIGHT//2 - (o.HEIGHT//2)//6 - TEXT_BOX_GUTTER), pygame.SRCALPHA)
        textbox.fill(C_TEXT_BOX)

        # Blit all 3
        screen.blit(get_image(o.currentBgPath), (0, 0))
        screen.blit(textbox, (0, o.HEIGHT//2 + (o.HEIGHT//2)//6))
        screen.blit(textbox, (0, 0))
        
        pygame.display.flip()
        clock.tick(o.FPS)
        sleep(0.1) # Make transition slower