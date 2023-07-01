import pygame

class Word_Image():
    def __init__(self,image):
        self.image = image
        self.rect = pygame.Rect((0,0),self.image.get_size())

    def draw(self, screen):
        screen.blit(self.image,self.rect)



class Text():
    def __init__(self,scale,image,space):
        order = " abcdefghijklmnopqrstuvwxyz,'.?!1234567890/\()"
        self.letters = {}
        self.lstart = None
        self.scale = scale
        self.space = space
        count = 0
        for pixel in range(image.get_width()):
            p = image.get_at((pixel,0))
            if self.lstart != None and p == (255,0,0):
                #get image letter
                dist = pixel - self.lstart -1
                height = image.get_height()
                pos= (self.lstart+1,0)
                # print(pos,(dist,height))
                letter = self.get_letter(image,pos,(dist,height))
                self.letters[order[count]] = letter
                count +=1
            if p == (255,0,0):
                self.lstart = pixel
            
    def get_letter(self, image, pos, size):
        letter = image.subsurface((pos,size))
        letter.set_colorkey((0,0,0))
        return letter

    def render(self,text,size=1,box = False,clr=None):
        if not box:
            string = str(text)
            surface = self.draw_line(string)
        else:
            words = str(text)
            words = words.split(" ")
            string_words = ""
            for i in words:
                string += i
            max_width = len(string_words) + self.space* (len(words)-1)
            if min(box) == 0:
                if box.index(max(box)) == 0:
                    


        #change colour if necessary
        if clr:
            surface = self.swap_pallet(surface,clr)

        surface = pygame.transform.scale(surface,(surface.get_width()*self.scale,surface.get_height()*self.scale))
        
        return Word_Image(surface)

    def draw_line(self,string):
        #get image width
        width = 0
        height = 0
        for s in string:
            width += self.letters[s].get_width()
            if self.letters[s].get_height() > height:
                height = self.letters[s].get_height()
        width += (len(string)-1) * self.space
        surface = pygame.Surface((width,height))
        #blitimage
        surface.fill((0,0,0)),surface.set_colorkey((0,0,0))
        # surface.set_alpha(self.image.get_alpha())
        x_offset = 0
        for char in string:
            surface.blit(self.letters[char],(x_offset, height - self.letters[char].get_height()))
            x_offset += self.letters[char].get_width() + self.space

        return surface


    def swap_pallet(self,surface,clr):
        img_copy = pygame.Surface(surface.get_size())
        img_copy.fill(clr)
        surface.set_colorkey((255,255,255))
        img_copy.blit(surface,(0,0))
        img_copy.set_colorkey((0,0,0))
        return img_copy


