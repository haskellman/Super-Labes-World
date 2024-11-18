# carrega todos os assets do jogo
def import_assets(self):
    self.tmx_maps = import_all_maps('.', 'data', 'maps')

    self.overworld_frames = {
        'characters': all_characters_import('.', 'graphics', 'characters'),
        'water': import_folder('.', 'graphics', 'tilesets', 'water'),
        'lake': lake_importer(3, 12, '.', 'graphics', 'tilesets', 'lake'),
    }
    self.fonts = {
        'dialog': pygame.font.Font(join('.', 'graphics', 'fonts', 'PixeloidSans.ttf'), 30),
        'bold': pygame.font.Font(join('.', 'graphics', 'fonts', 'dogicapixelbold.otf'), 20),
        'regular': pygame.font.Font(join('.', 'graphics', 'fonts', 'PixeloidSans.ttf'), 18),
        'regular_mid': pygame.font.Font(join('.', 'graphics', 'fonts', 'PixeloidSans.ttf'), 22),
        'regular_big': pygame.font.Font(join('.', 'graphics', 'fonts', 'PixeloidSans.ttf'), 34),
    }
    self.interface_frames = {
        'interface': import_folder_dict('.', 'graphics', 'interface'),
        'items': import_folder_dict('.', 'graphics', 'items'),
        'interactive_objects': import_folder_dict('.', 'graphics', 'interactive_objects'),
    }