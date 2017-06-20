import os
import pygame
from options import *

# COLORS
C_WHITE = [255, 255, 255]
C_RED = [255, 0, 0]
C_DARK_RED = (125,0,0)
C_GREEN = [0, 255, 0]
C_BLUE = [0, 0, 255]
C_BLACK = [0, 0, 0]
C_GREY = (128, 128, 128)
C_HOT_PINK = (255,51,153)

# LIBRARIES
# Source: http://www.nerdparadise.com/tech/python/pygame/basics/
_image_library = {}
def get_image(path, img_w = WIDTH, img_h = HEIGHT):
    global _image_library
    image = _image_library.get(path)
    if image == None:
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonicalized_path)
            image = pygame.transform.scale(image, (img_w, img_h))
            _image_library[path] = image
    return image

_sound_library = {}
def play_sound(path):
  global _sound_library
  sound = _sound_library.get(path)
  if sound == None:
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    sound = pygame.mixer.Sound(canonicalized_path)
    _sound_library[path] = sound
  sound.play()

_cached_text = {}
def create_text(text, size = TEXT_FONT_SIZE, color = C_BLACK):
    global _cached_text
    key = '|'.join(map(str, (size, color, text)))
    image = _cached_text.get(key, None)
    if image == None:
        font = pygame.font.Font('resources/fonts/Palatino.ttc', size)
        if ("\n" in text):
            images = []
            index = 0
            while "\n" in text:
                index = text.find('\n')
                images.append(font.render(text[:index], True, color))
                text = text[index+1:]
            images.append(font.render(text, True, color))
            _cached_text[key] = images
            ret = images
        else:
            font = pygame.font.Font('resources/fonts/Palatino.ttc', size)
            image = font.render(text, True, color)
            _cached_text[key] = image
            ret = image
        return ret
    else:
        return image

def create_bold_text(text, size = TITLE_FONT_SIZE, color = C_BLACK):
    global _cached_text
    key = '|'.join(map(str, (size, color, text)))
    image = _cached_text.get(key, None)
    if image == None:
        font = pygame.font.Font('resources/fonts/Palatino_Bold.otf', size)
        if ("\n" in text):
            images = []
            index = 0
            while "\n" in text:
                index = text.find('\n')
                images.append(font.render(text[:index], True, color))
                text = text[index+1:]
            images.append(font.render(text, True, color))
            _cached_text[key] = images
            ret = images
        else:
            font = pygame.font.Font('resources/fonts/Palatino_Bold.otf', size)
            image = font.render(text, True, color)
            _cached_text[key] = image
            ret = image
        return ret
    else:
        return image

# Used with temporary text. Images are not stored for long term
_cached_text_one = None
def print_text(text, size = TEXT_FONT_SIZE, color = C_BLACK, bold = False):
    global _cached_text_one
    if text is not _cached_text_one:
        if bold is True:
            font = pygame.font.Font('resources/fonts/Palatino_Bold.otf', size)
        else:
            font = pygame.font.Font('resources/fonts/Palatino.ttc', size)
        if ("\n" in text):
            images = []
            index = 0
            while "\n" in text:
                index = text.find('\n')
                images.append(font.render(text[:index], True, color))
                text = text[index+1:]
            images.append(font.render(text, True, color))
            _cached_text_one = images
            ret = images
        else:
            image = font.render(text, True, color)
            _cached_text_one = image
            ret = image
        return ret
    else:
        return _cached_text_one

# UTILITY FUNCTIONS
# Returns the width and height coordinates to fit the shape to the center of the screen.
# Width and height can be individually overriden, or set to -1 to be ignored.
def center_coords(shape, override_w = -1, override_h = -1):
    if override_w == -1:
        if override_h == -1: # Both w and h are default, get full center
            return (WIDTH // 2 - shape.get_width() // 2, HEIGHT // 2 - shape.get_height() // 2)
        else: # width is default, height is not
            return (WIDTH // 2 - shape.get_width() // 2, override_h)
    else:
        if override_h == -1: # height is default, width is not
            return (override_w, HEIGHT // 2 - shape.get_height() // 2)
        else: # Both w and h are overriden, why are you using this function?
            return (override_w, override_h)

# Returns a list of images to handle multi-line text. Wraps around a hardcoded width.
def wrap_text(text):
    ret = ""
    font = pygame.font.Font('resources/fonts/Palatino.ttc', TEXT_FONT_SIZE)

    while text:
        i = 1

        # determine maximum width of line
        # HARDCODED WRAP LENGTH HERE...v
        while font.size(text[:i])[0] < WIDTH-TEXT_MARGIN*2 and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        ret += text[:i].decode('utf-8')
        ret += "\n"

        # remove the text we just blitted
        text = text[i:]
    return ret

# Returns how many lines long a file is.
def file_len(fname):
    count = 0
    with open(fname) as f:
        for i, l in enumerate(f):
            if not(l[:10] == "background" or l[:5] == "music" or not l.strip()) :
                count += 1
    return count