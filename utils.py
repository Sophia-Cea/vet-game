import pygame
import sys
import os
import math
import random
import json
from datetime import datetime, timedelta

pygame.init()


def resize(image, scale):
    imgSize = image.get_size()
    imgSizeScaled = [imgSize[0]*scale, imgSize[1]*scale]
    return pygame.transform.smoothscale(image, imgSizeScaled)


sizeOptions = [[1600,900], [1920,1080], [2560, 1440], [3840, 2160]]

with open("jsonData/gamedata.json") as f:
    gameData = json.load(f)

with open("jsonData/patientInfo.json") as f:
    patientInfo = json.load(f)

with open("jsonData/potionInfo.json") as f:
    potionInfo = json.load(f)

with open("jsonData/plantData.json") as f:
    plantInfo = json.load(f)


class GameData:
    playerIngredients = gameData["playerIngredients"]
    gold = 0
    silver = 0
    copper = 0 
    newCustomerChance = 60
    # newCustomerChance = 200
    customerLimit = 3

    animalData = {
        "common" : {
            # "mouse" : 10,
            "paige" : 10,
            "cat" : 20,
            # "dog" : 10,
            "rabbit" : 10,
            # "squirrel" : 10
        },
        "rare" : {
            "wolf" : 5,
            # "panther" : 5,
            # "salamander" : 5,
        },
        "uncommon" : {
            "fox" : 3,
            "owl" : 3,
            # "crow" : 3,
        },
        "super rare" : {
            "unicorn" : 2,
            # "crystal fox" : 2,
        },
        "legendary" : {
            "dragon" : 1,
        }
    }

    potionsInInventory = [
        {
            "name": "potionOfRed",
            "quantity" : 1
        },
        {
            "name": "potionOfBlue",
            "quantity" : 1
        } 
    ]

    seedInventory = [
        {
            "name" : "plant1",
            "quantity" : 2
        },
        {
            "name" : "plant2",
            "quantity" : 3
        }
    ]

    gardenData = {
        "garden 1" : {
            "locked" : False,
            "plots" : [
                None,
                None,
                None
            ]
        },
        "garden 2" : {
            "locked" : True,
            "plots" : [
                None,
                None,
                None
            ]
        }
    }

    patientsInRooms = [
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None
    ]

    roomData = [
        {
            "locked": False,
            "patient" : None
        },
        {
            "locked": False,
            "patient" : None
        },
        {
            "locked": True,
            "patient" : None
        },
        {
            "locked": True,
            "patient" : None
        },
        {
            "locked": True,
            "patient" : None
        },
        {
            "locked": True,
            "patient" : None
        },
        {
            "locked": True,
            "patient" : None
        },
        {
            "locked": True,
            "patient" : None
        }
    ]

    activePatients = [
    ]


def sum_animal_values(data):
    total = []
    for category in data.values():
        for key, value in category.items():
            for _ in range(value):
                total.append(key)
    return total






orig_size = sizeOptions[0]

WIDTH = 1600
HEIGHT = 900
delta = 1
scaleFactor = WIDTH/orig_size[0]


def gradient(col1, col2, surface, rect=None):
    if rect == None:
        rect = pygame.Rect(0,0, surface.get_width(), surface.get_height())

    if type(col1) != tuple:
        col1 = col1.copy()
    if type(col2) != tuple:
        col2 = col2.copy()
    inc1 = (col2[0] - col1[0])/rect.height
    inc2 = (col2[1] - col1[1])/rect.height
    inc3 = (col2[2] - col1[2])/rect.height
    color = [col1[0], col1[1], col1[2]]
    for i in range(rect.height):
        pygame.draw.line(surface, color, (rect.x, rect.y + i), (rect.width, rect.y + i), 2)
        color[0] += inc1
        color[1] += inc2
        color[2] += inc3

def resource_path(relative_path):
  if hasattr(sys, '_MEIPASS'):
      return os.path.join(sys._MEIPASS, relative_path)
  return os.path.join(os.path.abspath('.'), relative_path)


class TextRenderer:
    """
    A class for rendering text in Pygame that caches rendered text surfaces
    to improve performance and reduce energy consumption.
    """
    def __init__(self):
        """
        Initializes the TextRenderer and the cache.
        It's assumed that pygame.init() has been called beforehand.
        """
        # Ensure the pygame font module is initialized
        if not pygame.font.get_init():
            pygame.font.init()
        
        # The cache will store already-rendered text surfaces.
        # The key will be a tuple (text, size, color, font_name)
        # and the value will be the rendered pygame.Surface and its pygame.Rect.
        self._cache = {}

    def render(self, surface, text, pos, size, color, font_name=None, align="topleft"):
        """
        Renders text onto a given surface.

        Args:
            surface (pygame.Surface): The surface to draw the text on.
            text (str): The text content to render.
            pos (tuple): A tuple (x, y) for the position of the text.
            size (int): The font size.
            color (tuple): An RGB tuple (r, g, b) for the text color.
            font_name (str, optional): The path to a .ttf font file or the name
                                       of a system font. Defaults to Pygame's
                                       default font.
            align (str, optional): The alignment of the text relative to the pos.
                                   Can be any of the pygame.Rect attributes like
                                   "topleft", "center", "midright", etc.
                                   Defaults to "topleft".
        """
        # 1. Create a unique key for the requested text properties.
        cache_key = (text, size, color, font_name)

        # 2. Check if the rendered text is already in the cache.
        if cache_key in self._cache:
            # If it is, retrieve the pre-rendered surface and rect.
            text_surface, text_rect = self._cache[cache_key]
        else:
            # 3. If not in cache, render it for the first time.
            try:
                # Create the font object.
                font = pygame.font.Font('fonts/Metamorphous-Regular.ttf', size)
            except FileNotFoundError:
                # If the specified font is not found, fall back to the default font.
                print(f"Warning: Font '{font_name}' not found. Using default font.")
                font = pygame.font.Font(None, size)
            
            # Render the text surface. 'True' for anti-aliasing.
            text_surface = font.render(text, True, color)
            
            # Get the rectangle of the rendered surface.
            text_rect = text_surface.get_rect()
            
            # 4. Store the newly rendered surface and rect in the cache.
            self._cache[cache_key] = (text_surface, text_rect)

        # 5. Set the position of the text rectangle using the specified alignment.
        # This uses Python's setattr to dynamically set the rect's attribute
        # (e.g., text_rect.center = pos or text_rect.topleft = pos).
        if hasattr(text_rect, align):
            setattr(text_rect, align, pos)
        else:
            print(f"Warning: Invalid alignment attribute '{align}'. Defaulting to 'topleft'.")
            text_rect.topleft = pos

        # 6. Blit (draw) the text surface onto the target surface.
        surface.blit(text_surface, text_rect)

    def clear_cache(self):
        """
        Clears the text cache. This can be useful if you need to free up memory,
        for example, when changing levels in a game where the on-screen text
        changes completely.
        """
        self._cache.clear()

textRenderer = TextRenderer()









