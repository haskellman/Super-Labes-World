import pygame
from pygame.math import Vector2 as vector 

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
ANIMATION_SPEED = 6
TILE_SIZE = 64 
VISITED_MAPS = []

COLORS = {
	'white': '#f4fefa', 
	'pure white': '#ffffff',
	'dark': '#2b292c',
	'light': '#c8c8c8',
	'gray': '#3a373b',
	'gold': '#ffd700',
	'light-gray': '#4b484d',
	'fire':'#f8a060',
	'water':'#50b0d8',
	'plant': '#64a990', 
	'black': '#000000', 
	'red': '#f03131',
	'blue': '#66d7ee'
}

GAME_LAYERS = {
	'water': 0,
	'bg': 1,
	'shadow': 2,
	'main': 3,
	'top': 4
}
