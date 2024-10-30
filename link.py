from game_data import COMPUTER_DATA
from support import import_folder_dict

class Link:
    def __init__(self, id):
        interface_frames =  import_folder_dict('.', 'graphics', 'links')
        self.title = COMPUTER_DATA[id]['title']
        self.description = COMPUTER_DATA[id]['description']
        self.icon = interface_frames[id]
        self.url = COMPUTER_DATA[id]['url']
        self.color = COMPUTER_DATA[id]['color']
