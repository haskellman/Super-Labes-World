from settings import *
from os.path import join
from os import walk
from pytmx.util_pygame import load_pygame

def import_image(*path, alpha = True, format = 'png'):
	full_path = join(*path) + f'.{format}'
	surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
	return surf

def import_character(cols, rows, *path):
    frame_dict = import_tilemap(rows, cols, *path)
    new_dict = {}
    for row, direction in enumerate(('down', 'left', 'right', 'up')):
        new_dict[direction] = [frame_dict[col, row] for col in range(cols)]
        new_dict[f'{direction}_idle'] = [frame_dict[(0, row)]]
    return new_dict 

def import_tilemap(cols, rows, *path):
	frames = {}
	surf = import_image(*path)
	cell_width, cell_height = surf.get_width() / cols, surf.get_height() / rows
	for col in range(cols):
		for row in range(rows):
			cutout_rect = pygame.Rect(col * cell_width, row * cell_height,cell_width,cell_height)
			cutout_surf = pygame.Surface((cell_width, cell_height))
			cutout_surf.fill('green')
			cutout_surf.set_colorkey('green')
			cutout_surf.blit(surf, (0,0), cutout_rect)
			frames[(col, row)] = cutout_surf
	return frames

def all_characters_import(*path):
    frames = {}
    for _, __, image_names in walk(join(*path)):
        for image in image_names:
            image_name = image.split('.')[0]
            frames[image_name] = import_character(4, 4, *path, image_name)
    return frames
