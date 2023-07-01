import pygame,math

class Word_Image():
    def __init__(self,image):
        self.image = image
        self.rect = pygame.Rect((0,0),self.image.get_size())

    def draw(self, screen):
        screen.blit(self.image,self.rect)

class Text():
    def __init__(self,scale,image,spacing):
        order = " abcdefghijklmnopqrstuvwxyz,'.?!1234567890/\()"
        self.letters = {}
        self.lstart = None
        self.scale = scale
        self.spacing = spacing
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

        self.space = self.letters[' '].get_width() + self.spacing
            
    def get_letter(self, image, pos, size):
        letter = image.subsurface((pos,size))
        letter.set_colorkey((0,0,0))
        return letter

    def get_lengths(self,words,size):
        lengths = []
        for word in words:
            length = 0
            for let in word:
                length += (self.letters[let].get_width()+self.spacing)*size 
            lengths.append(length)
        return lengths

    def render(self,text,size=1,box = False,clr=None):
        if not box:
            string = str(text)
            surface = self.draw_line(string,size)
        else:
            # if text box
            words = str(text)
            words = words.split(" ")
            lengths = self.get_lengths(words,size)
            print(lengths)
            if min(box) == 0:
                if box.index(max(box)) == 0:
                    height = self.letters[" "].get_height()
                    width = 0
                    BoxWidth = box[0]
                    NumLines = 1
                    lines = []
                    #getting size
                    line = ""
                    for index,word in enumerate(lengths):
                        if not line:
                            twidth = width + word
                            WordLength = word
                        else:
                            twidth = width + self.space + word
                            WordLength = word + self.space
                        if twidth <= BoxWidth:
                            width += WordLength
                            if line:
                                line += " " +words[index]
                            else:
                                line += words[index]
                        elif WordLength > BoxWidth:
                            print(words[index])
                        else:
                            NumLines += 1
                            width = 0
                            lines.append(line)
                            line = ""
                    lines.append(line)

                    print(lines)

                    #creating surface & drawing
                    surface = pygame.Surface((BoxWidth,(height+1)*NumLines))
                    for index,li in enumerate(lines):
                        surface.blit(self.draw_line(li,size),(0,index*(height+1)))

        #change colour if necessary
        if clr:
            surface = self.swap_pallet(surface,clr)

        surface = pygame.transform.scale(surface,(surface.get_width()*self.scale,surface.get_height()*self.scale))
        
        return Word_Image(surface)

    def draw_line(self,string,size):
        #get image width
        width = 0
        height = self.letters[" "].get_height()
        for s in string:
            width += self.letters[s].get_width()
        width += (len(string)-1) * self.spacing
        surface = pygame.Surface((width,height))
        #blitimage
        surface.fill((0,0,0)),surface.set_colorkey((0,0,0))
        # surface.set_alpha(self.image.get_alpha())
        x_offset = 0
        for char in string:
            surface.blit(self.letters[char],(x_offset, height - self.letters[char].get_height()))
            x_offset += self.letters[char].get_width() + self.spacing

        surface = pygame.transform.scale(surface,(surface.get_width()*size,surface.get_height()*size))

        return surface

    def swap_pallet(self,surface,clr):
        img_copy = pygame.Surface(surface.get_size())
        img_copy.fill(clr)
        surface.set_colorkey((255,255,255))
        img_copy.blit(surface,(0,0))
        img_copy.set_colorkey((0,0,0))
        return img_copy


