import pygame
import os
import sys
import json
import datetime
from time import sleep

# Import all supporting files
from my_lib import *
from transitions import *

pygame.init()
screen = pygame.display.set_mode((o.WIDTH, o.HEIGHT))
pygame.mixer.init()

clock = pygame.time.Clock()


# PROGRAM VARS
layout = "TITLE" # Which screen is the user viewing?
doGameLoop = True # Is the game running?
isMusicPlaying = False # Is music playing?
global meta
meta = None # What does _meta.json say?
with open("_meta.json") as metaFile:
    meta = json.load(metaFile)

# TITLE VARS
titleSelected = 0 # 0:play, 1:continue, 2:options, 3:credits, 4:exit
titleBgPath = ""
titleMusicPath = ""

# CONTINUE VARS
continueSelected = 0 # 0:yes, 1:no
isStartingFromContinue = False # Is the player playing the game from a previous save?
continueStartPoint = 0 # What line of the story file to continue from?
continueConfirm = False # Is the user trying to start a new game which will override the saved game?

# GAME VARS
line = ""
lineIndex = 1
contentIndex = 0
doIncrementContentIndex = False


# ERROR VARS
isErrorMusicPlaying = False


# Get data for title and credits screens from cover.txt
with open("cover.txt") as cover:
    isCredits = False
    cover_credits = ""
    for cover_line in cover:
        if isCredits:
            cover_credits += cover_line
        elif cover_line[:5] == "title":
            cover_title = cover_line[6:].strip()
        elif cover_line[:9] == "menu song":
            o.currentMusicPath = "resources/music/%s.mp3" % cover_line[10:].strip()
            titleMusicPath = o.currentMusicPath
        elif cover_line[:10] == "menu image":
            o.currentBgPath = "resources/bg/%s.png" % cover_line[11:].strip()
            titleBgPath = o.currentBgPath
        elif cover_line[:7] == "credits":
            isCredits = True

while doGameLoop:

    pygame.display.flip()
    clock.tick(o.FPS)

    if (layout is "TITLE"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                doGameLoop = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if (titleSelected < 4):
                    play_sound('resources/sfx/button_press.wav')
                    if titleSelected == 0 and meta["save"]["lastLine"] == 0:
                        titleSelected += 2
                    else:
                        titleSelected += 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if (titleSelected > 0):
                    play_sound('resources/sfx/button_press.wav')
                    if titleSelected == 2 and meta["save"]["lastLine"] == 0:
                        titleSelected -= 2
                    else:
                        titleSelected -= 1
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                play_sound('resources/sfx/button_press.wav')
                if (titleSelected == 0):
                    if meta["save"]["lastLine"] == 0: # Starting a fresh new game
                        layout = "STORY"
                        # This "reset the story" code is repeated on the Continue screen.
                        # Set start date in meta file
                        today = datetime.datetime.now()
                        timeSuffix = "AM"
                        hours = today.hour
                        if hours > 12:
                            hours = hours % 12
                            timeSuffix = "PM"
                        meta["save"]["dateCreated"] = today.strftime('%m/%d/%y, ') + str(hours) + today.strftime(':%M') + timeSuffix
                        with open('_meta.json', 'w') as metaFile:
                            metaFile.write(json.dumps(meta))
                        # Open the story file and prepare the first line
                        lineIndex = 0
                        contentIndex = 0
                        f = open("story.txt")
                        line = f.readline()
                    else: # Notify the user that they are about to override a save
                        layout = "CONTINUE"
                        continueConfirm = True
                        continueStartPoint = meta["save"]["lastLine"]
                        continueSelected = 0
                elif (titleSelected == 1):
                    layout = "CONTINUE"
                    continueStartPoint = meta["save"]["lastLine"]
                    continueSelected = 0
                elif (titleSelected == 2):
                    layout = "OPTIONS"
                elif (titleSelected == 3):
                    layout = "CREDITS"
                elif (titleSelected == 4):
                    doGameLoop = False
        # Set music
        if isMusicPlaying is False:
            pygame.mixer.music.load(titleMusicPath)
            pygame.mixer.music.play(-1)
            isMusicPlaying = True

        # Set background
        screen.blit(get_image(titleBgPath), (0, 000))

        textbox = pygame.Surface((o.WIDTH//2, ELEMENT_SPACING*5), pygame.SRCALPHA)
        textbox.fill(C_TITLE_BOX)
        screen.blit(textbox, (o.WIDTH//4, o.HEIGHT//2))

        # Draw selector
        selectorbox = pygame.Surface((o.WIDTH//2, ELEMENT_SPACING), pygame.SRCALPHA)
        selectorbox.fill(C_SELECTOR_BOX)
        screen.blit(selectorbox, (o.WIDTH//4, o.HEIGHT//2 + ELEMENT_SPACING * titleSelected))

        # Draw text
        title_txt = create_bold_text(cover_title, ELEMENT_FONT_SIZE * 3, C_DARK_RED)
        play_button = create_bold_text("Start", ELEMENT_FONT_SIZE, C_WHITE)
        if meta["save"]["lastLine"] == 0:
            continue_button = create_bold_text("Continue", ELEMENT_FONT_SIZE, C_GREY)
        else:
            continue_button = create_bold_text("Continue", ELEMENT_FONT_SIZE, C_WHITE)
        options_button = create_bold_text("Options", ELEMENT_FONT_SIZE, C_WHITE)
        credits_button = create_bold_text("Credits", ELEMENT_FONT_SIZE, C_WHITE)
        exit_button = create_bold_text("Exit", ELEMENT_FONT_SIZE, C_WHITE)
        screen.blit(title_txt, center_coords(title_txt, -1, o.HEIGHT//5))
        screen.blit(play_button, center_coords(play_button, -1, o.HEIGHT//2))
        screen.blit(continue_button, center_coords(continue_button, -1, o.HEIGHT//2 + ELEMENT_SPACING))
        screen.blit(options_button, center_coords(options_button, -1, o.HEIGHT//2 + ELEMENT_SPACING * 2))
        screen.blit(credits_button, center_coords(credits_button, -1, o.HEIGHT//2 + ELEMENT_SPACING * 3))
        screen.blit(exit_button, center_coords(exit_button, -1, o.HEIGHT//2 + ELEMENT_SPACING * 4))


    elif (layout is "STORY"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                doGameLoop = False
                f.close()
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                play_sound('resources/sfx/button_press.wav')
                if inTransition:
                    inTransition = False
                else:
                    line = f.readline()
                    lineIndex+=1
                    doIncrementContentIndex = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                layout = "TITLE"
                f.close()
                titleSelected = 0
                isMusicPlaying = False
                # Update meta file with saved game
                fileLen = file_len('story.txt')
                meta["save"]["lastLine"] = lineIndex
                meta["save"]["progressPercentage"] = contentIndex * 100 // fileLen
                with open('_meta.json', 'w') as metaFile:
                    metaFile.write(json.dumps(meta))

        # If we're loading a continue, fast forward through the text to get to where we left off
        if isStartingFromContinue:
            isStartingFromContinue = False
            for i in range(continueStartPoint):
                if line[:11] == "$background": # Handle setting new background
                    o.currentBgPath = "resources/bg/%s.png" % line[12:].strip()
                elif line[:6] == "$music": # Handle setting new tunes
                    command = line[7:].strip()
                    if (command == "OFF"):
                        isMusicPlaying = False
                    else:
                        isMusicPlaying = True
                        o.currentMusicPath = "resources/music/%s.mp3" % command
                line = f.readline()
            # Load new song
            if isMusicPlaying:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(o.currentMusicPath)
                pygame.mixer.music.play(-1)

        # Now start reading the file line by line, parsing as we go.
        if line == "": # If we reach the end of the file, go back to end.
            layout = "CREDITS"
            f.close()
            isMusicPlaying = False
            # Erase old save now that the player has finished
            lineIndex = 0
            contentIndex = 0
            meta["save"]["lastLine"] = 0
            meta["save"]["progressPercentage"] = 0
            with open('_meta.json', 'w') as metaFile:
                metaFile.write(json.dumps(meta))
        else:
            if line == "\n" or line[:2] == "//": # If it's a blank line or comment, skip to the next one.
                line = f.readline()
                lineIndex+=1
            elif line[:11] == "$background": # Handle setting new background
                temp = line[12:].strip()
                if not temp == []: # Make sure it's not a blank line
                    o.currentBgPath = "resources/bg/%s.png" % line[12:].strip()
                line = f.readline()
                lineIndex+=1
            elif line[:6] == "$music": # Handle setting new tunes
                command = line[7:].strip()
                print("'%s' '%s'" % (command, isMusicPlaying))
                if not temp == []: # Make sure it's not a blank line
                    if command == "OFF":
                        isMusicPlaying = False
                        pygame.mixer.music.stop()
                    elif (command == "PAUSE" and isMusicPlaying is True):
                        isMusicPlaying = False
                        pygame.mixer.music.pause()
                    elif (command == "UNPAUSE" and isMusicPlaying is False):
                        isMusicPlaying = True
                        pygame.mixer.music.unpause()
                    else:
                        o.currentMusicPath = "resources/music/%s.mp3" % line[7:].strip()
                        isMusicPlaying = True
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(o.currentMusicPath)
                        pygame.mixer.music.play(-1)
                line = f.readline()
                lineIndex+=1
            elif line[:11] == "$transition": # Handle transition commands
                # If two transitions are listed together and one causes user to wait, then make it happen.
                if inTransition:
                    inTransitionBg = pygame.Surface((o.WIDTH, o.HEIGHT))
                    inTransitionBg.fill(transitionBg)
                    screen.blit(inTransitionBg, (0, 0))
                else:
                    temp = line[12:].strip().split()
                    if not temp == []: # Make sure it's not a blank line
                        if temp[0] == "fadeto":
                            inTransition = True # This needs to be run before calling the transition function
                            if len(temp) == 1: # If no color listed, use default black
                                transition_fadeto(screen, clock)
                            else: # If color is given, use that color
                                transition_fadeto(screen, clock, temp[1])
                        elif temp[0] == "fadefrom":
                            # inTransition not called because user immediately moves to content when exiting transition
                            if len(temp) == 1: # If no color listed, use default black
                                transition_fadefrom(screen, clock)
                            else: # If color is given, use that color
                                transition_fadefrom(screen, clock, temp[1])
                        elif temp[0] == "fadetoandfrom":
                            # inTransition not called because user immediately moves to content when exiting transition
                            if len(temp) == 1: # If no color listed, use default black
                                transition_fadetoandfrom(screen, clock)
                            elif len(temp) == 2: # If color (and no time) is given, use that color
                                transition_fadetoandfrom(screen, clock, temp[1])
                            else: # If color and time are given, use those
                                transition_fadetoandfrom(screen, clock, temp[1], temp[2])
                    line = f.readline()
                    lineIndex+=1
            else: # Some thigns always happen
                if doIncrementContentIndex:
                    doIncrementContentIndex = False
                    contentIndex+=1

                if inTransition:
                    inTransitionBg = pygame.Surface((o.WIDTH, o.HEIGHT))
                    inTransitionBg.fill(transitionBg)
                    screen.blit(inTransitionBg, (0, 0))
                else:
                    # Set background
                    screen.blit(get_image(o.currentBgPath), (0, 0))

                    # Set text box bg
                    textbox = pygame.Surface((o.WIDTH, o.HEIGHT//2 - (o.HEIGHT//2)//6 - TEXT_BOX_GUTTER), pygame.SRCALPHA)
                    textbox.fill(C_TEXT_BOX)
                    screen.blit(textbox, (0, o.HEIGHT//2 + (o.HEIGHT//2)//6))
                    if line[:1] == ":": # Handle a narrative line
                        # Set text
                        wrappedText = wrap_text(line[1:].strip())
                        text = print_text(wrappedText, TEXT_FONT_SIZE, C_WHITE)

                        if (isinstance(text, list)):
                            hOffset = 0
                            for t in text:
                                screen.blit(t, (TEXT_MARGIN, o.HEIGHT//2 + (o.HEIGHT//2)//6 + TEXT_MARGIN*2 + hOffset))
                                hOffset += TEXT_FONT_SIZE
                        else:
                            screen.blit(text, (TEXT_MARGIN, o.HEIGHT//2 + (o.HEIGHT//2)//6 + TEXT_MARGIN*2))
                    else:
                        colonIndex = line.find(":")

                        # Set character name
                        title = print_text(line[:colonIndex].strip(), TITLE_FONT_SIZE, C_WHITE, True)
                        screen.blit(title, (TEXT_MARGIN, o.HEIGHT//2 + (o.HEIGHT//2)//6 + TEXT_MARGIN))

                        # Set text
                        wrappedText = wrap_text(line[colonIndex+1:].strip())
                        text = print_text(wrappedText, TEXT_FONT_SIZE, C_WHITE)
                        if (isinstance(text, list)):
                            hOffset = 0
                            for t in text:
                                screen.blit(t, (TEXT_MARGIN, o.HEIGHT//2 + (o.HEIGHT//2)//6 + TEXT_MARGIN*2 + title.get_height() + hOffset))
                                hOffset += TEXT_FONT_SIZE
                        else:
                            screen.blit(text, (TEXT_MARGIN, o.HEIGHT//2 + (o.HEIGHT//2)//6 + TEXT_MARGIN*2 + title.get_height()))


    elif (layout is "CONTINUE"):
        # This is set before event testing to avoid seeing 1 frame of the "continue from last save" screen when trying to override save.
        # Set background
        screen.blit(get_image(titleBgPath), (0, 000))
        # Draw title prompt
        if continueConfirm:
            continue_raw = "You have an old save that will be overridden!\nStarted on %s (%s%% completed)\nAre you sure you want to proceed?" % (meta["save"]["dateCreated"], meta["save"]["progressPercentage"])
        else:
            continue_raw = "Continue from last save?\nStarted on %s (%s%% completed)" % (meta["save"]["dateCreated"], meta["save"]["progressPercentage"])
        continue_txt = create_text(continue_raw, ELEMENT_FONT_SIZE, C_DARK_RED)
        hOffset = 0
        for t in continue_txt:
            screen.blit(t, center_coords(t, -1, o.HEIGHT//5 + hOffset))
            hOffset += ELEMENT_FONT_SIZE


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                doGameLoop = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if continueSelected == 0: # If "yes" is selected
                    play_sound('resources/sfx/button_press.wav')
                    layout = "STORY"
                    if continueConfirm: # If we are here from pressing "Start"
                        continueConfirm = False
                        isStartingFromContinue = False
                        # Set start date in meta file
                        today = datetime.datetime.now()
                        timeSuffix = "AM"
                        hours = today.hour
                        if hours > 12:
                            hours = hours % 12
                            timeSuffix = "PM"
                        meta["save"]["dateCreated"] = today.strftime('%m/%d/%y, ') + str(hours) + today.strftime(':%M') + timeSuffix
                        with open('_meta.json', 'w') as metaFile:
                            metaFile.write(json.dumps(meta))
                        # Open the story file and prepare the first line
                        lineIndex = 0
                        contentIndex = 0
                        f = open("story.txt")
                        line = f.readline()
                    else: # If we are here from pressing "Continue"
                        isStartingFromContinue = True
                        lineIndex = meta["save"]["lastLine"]
                        f = open("story.txt")
                        line = f.readline()
                else: # If "no" is selected
                    play_sound('resources/sfx/button_press.wav')
                    layout = "TITLE"
                    continueConfirm = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if (continueSelected < 1):
                    play_sound('resources/sfx/button_press.wav')
                    continueSelected += 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if (continueSelected > 0):
                    play_sound('resources/sfx/button_press.wav')
                    continueSelected -= 1

        # Draw button background
        textbox = pygame.Surface((o.WIDTH//2, ELEMENT_SPACING*2), pygame.SRCALPHA)
        textbox.fill(C_TITLE_BOX)
        screen.blit(textbox, (o.WIDTH//4, o.HEIGHT//2))

        # Draw selector
        selectorbox = pygame.Surface((o.WIDTH//2, ELEMENT_SPACING), pygame.SRCALPHA)
        selectorbox.fill(C_SELECTOR_BOX)
        screen.blit(selectorbox, (o.WIDTH//4, o.HEIGHT//2 + ELEMENT_SPACING * continueSelected))

        # Draw buttons
        continue_yes = create_bold_text("Yes", ELEMENT_FONT_SIZE, C_WHITE)
        continue_no = create_bold_text("No", ELEMENT_FONT_SIZE, C_WHITE)
        screen.blit(continue_yes, center_coords(continue_yes, -1, o.HEIGHT//2))
        screen.blit(continue_no, center_coords(continue_no, -1, o.HEIGHT//2 + ELEMENT_SPACING))

    elif (layout is "OPTIONS"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                doGameLoop = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                play_sound('resources/sfx/button_press.wav')
                layout = "TITLE"
        # Clear event queue then test for debug shortcut
        # Break the game by holding the keys that spell "sonic".
        while pygame.event.get(): pass
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] and keys[pygame.K_o] and keys[pygame.K_n] and keys[pygame.K_i] and keys[pygame.K_c]:
            layout = "iamerror"


        screen.blit(get_image('resources/bg/title_bg.png'), (0, 000))
        
        text = create_text("Options here.", 24, C_BLACK)
        screen.blit(text, center_coords(text))


    elif (layout is "CREDITS"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                doGameLoop = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                play_sound('resources/sfx/button_press.wav')
                layout = "TITLE"
                titleSelected = 0

        # Set music
        if isMusicPlaying is False:
            pygame.mixer.music.load(titleMusicPath)
            pygame.mixer.music.play(-1)
            isMusicPlaying = True

        screen.blit(get_image('resources/bg/title_bg.png'), (0, 000))
        text = create_text(cover_credits, CREDIT_FONT_SIZE, C_WHITE)
        if (isinstance(text, list)):
            hOffset = o.HEIGHT//2
            for t in text:
                screen.blit(t, center_coords(t, 25, hOffset))
                hOffset += CREDIT_FONT_SIZE
        else:
            screen.blit(text, center_coords(text, 25))

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                doGameLoop = False
        if not isErrorMusicPlaying:
            isErrorMusicPlaying = True
            pygame.mixer.music.stop()
            pygame.mixer.music.load("resources/music/iamerror.mp3")
            pygame.mixer.music.play(-1)
        screen.blit(get_image('resources/bg/iamerror.png'), (0, 000))
        text = create_bold_text("How did you get here?", 100, C_HOT_PINK)
        screen.blit(text, center_coords(text))