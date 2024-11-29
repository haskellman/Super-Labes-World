
from pytmx.util_pygame import load_pygame
import pygame

pygame.init()
pygame.display.set_mode((800, 600))
tiled_map = load_pygame('example.tmx')

for layer in tiled_map.layers:
    print(layer.name)
    if layer.name == 'Objects':
        for obj in layer:
            print(obj.name)
            print(obj.x)
            print(obj.y)
            print(obj.width)
            print(obj.height)
            print(obj.properties)
    