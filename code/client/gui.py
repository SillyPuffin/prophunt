import pygame,math

class Word_Image():
    def __init__(self,image):
        self.image = image
        self.rect = pygame.Rect((0,0),self.image.get_size())

    def draw(self, screen):
        screen.blit(self.image,self.rect)

class TextBox():
    def __init__(self,text,box):
        self.texts = text
        self.box = box
        self.rect = self.box.get_rect()
        self.box.blit(self.texts,(0,0))
        self.image = self.box.copy()
        self.scroll = 0
        self.max_scroll= -abs(self.box.get_height() - self.texts.get_height())

    def update(self,events,mouse,screen):
        if self.rect.collidepoint(mouse):
            for event in events:
                if event.type == pygame.MOUSEWHEEL:
                    self.scroll += event.y * 16
        if self.scroll < self.max_scroll:
            self.scroll = self.max_scroll
        if self.scroll > 0:
            self.scroll = 0

        self.box.fill(0)
        self.box.blit(self.texts,(0,self.scroll))
        self.image = self.box.copy()
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
                if let != '\n':
                    length += (self.letters[let].get_width()+self.spacing)*size 
            lengths.append(length)
        return lengths

    def render(self,text,size=1,box = False,clr=None):
        if not box:
            string = str(text)
            surface = self.draw_line(string,size)
        else:
            # if text box
            FixedTextbox = False
            words = str(text)
            words = words.split(" ")
            lengths = self.get_lengths(words,size)
            if min(box) == 0:
                if box.index(max(box)) == 0:
                    surface = self.draw_textbox(words,lengths,size, box)
            else:
                FixedTextbox = True
                surface = self.draw_textbox(words,lengths,size,box)
        #change colour if necessary
        if clr:
            surface = self.swap_pallet(surface,clr)
        #scaling to scale
        surface = self.scale_image(surface,self.scale)

        if FixedTextbox:
            _class = TextBox(surface,pygame.Surface((box[0]*self.scale,box[1]*self.scale)))
        else:
            _class = Word_Image(surface)
        return _class
    
    def draw_textbox(self,words, lengths, size,box):
        height = self.letters[" "].get_height()
        width = 0
        BoxWidth = box[0]
        NumLines = 1
        lines = []
        #getting size
        line = ""
        for index,word in enumerate(lengths):
            if not line:
                WordLength = word
            else:
                WordLength = word + self.space
            twidth = self.GetLengthString(line+" " + words[index],size)
            #adding borders 
            if twidth <= BoxWidth:
                # width += WordLength
                string = words[index]
                if line:
                    line += " "
                    width += self.space
                lines,line,NumLines,width = self.AddWordToLine(lines,line,NumLines,width,string)

            elif WordLength > BoxWidth:
                for letter in words[index]:
                    if letter != '\n' and width + (self.letters[letter].get_width() + self.spacing)*size <= BoxWidth:
                        line += letter
                        width += (self.letters[letter].get_width() + self.spacing)*size
                    else:
                        NumLines += 1
                        lines.append(line)
                        line = ""
                        width = 0
                        if letter != '\n':
                            line += letter
                            width = (self.letters[letter].get_width() + self.spacing) * size
            else:
                NumLines += 1
                lines.append(line)
                line = ""
                lines,line,NumLines,width = self.AddWordToLine(lines,line,NumLines,width, words[index])
        lines.append(line)
        #creating surface & drawing
        surface = pygame.Surface((BoxWidth,(height+1)*size*NumLines))
        for index,li in enumerate(lines):
            surface.blit(self.draw_line(li,size),(0,index*(height+1)*size))
        
        return surface

    def scale_image(self,surface,amount):
        surface = pygame.transform.scale(surface,(surface.get_width()*amount,surface.get_height()*amount))
        return surface

    def AddWordToLine(self,lines,line,NumLines,width,word):
        for letter in word:
            if letter != "\n":
                line += letter
                width += self.letters[letter].get_width() + self.spacing
            else:
                NumLines += 1
                lines.append(line)
                line = ""
                width = 0
        return lines,line,NumLines,width    

    def GetLengthString(self,string, size):
        width = 0
        for letter in string:
            if letter != "\n":
                width += (self.letters[letter].get_width() + self.spacing)*size
        return width

    def draw_line(self,string,size):
        #get image width
        width = 0
        height = self.letters[" "].get_height()
        for s in string:
            if s != "\n":
                width += self.letters[s].get_width()
        if string:    
            width += (len(string)-1) * self.spacing
        else:
            width = 0
        surface = pygame.Surface((width,height))
        #blitimage
        surface.fill((0,0,0)),surface.set_colorkey((0,0,0))
        # surface.set_alpha(self.image.get_alpha())
        x_offset = 0
        for char in string:
            if char != "\n":
                surface.blit(self.letters[char],(x_offset, height - self.letters[char].get_height()))
                x_offset += self.letters[char].get_width() + self.spacing

        #scaling to size
        surface = self.scale_image(surface,size)

        return surface

    def swap_pallet(self,surface,clr):
        img_copy = pygame.Surface(surface.get_size())
        img_copy.fill(clr)
        surface.set_colorkey((255,255,255))
        img_copy.blit(surface,(0,0))
        img_copy.set_colorkey((0,0,0))
        return img_copy


