from .utils import *

class Images:
    def __init__(self,scale):
        self.tiles = load_folder('graphics/tiles',scale,False,(0,0,0))
        print(self.tiles)
        self.tile_sets = {
            'wood': load_page('graphics/tiles/pages/wood_page.png',(160,160,160),(20,20),scale)
        }
        