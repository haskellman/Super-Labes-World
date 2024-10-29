
from game_data import ITEMS_DATA
from support import import_folder_dict



class Item:
    def __init__(self, id):
        inventory_frames =  import_folder_dict('.', 'graphics', 'items')
        self.name = ITEMS_DATA[id]['name']
        self.description = ITEMS_DATA[id]['description']
        self.item_icon = inventory_frames[id]

    def on_take(self):
        print(f'You have picked up {self.name}')

    def __str__(self):
        return f'{self.name}: {self.description}'