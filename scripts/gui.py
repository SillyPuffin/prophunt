import pygame,math
from pygame.math import Vector2 as vec
from pygame.mouse import get_pressed as mouse_buttons
from .utils import *

class Word_Image():
    def __init__(self,image):
        self.image = image
        self.rect = pygame.Rect((0,0),(self.image.get_width(),self.image.get_height()))

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

    def update(self,events,mouse,game):
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

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class Text():
    def __init__(self,scale,image,spacing):
        order = " abcdefghijklmnopqrstuvwxyz,'.:-?!1234567890/\()[]<>"
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
        FixedTextbox = False
        size = size * self.scale
        box = scale(self.scale,box)
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
        # surface = self.scale_image(surface,self.scale)

        surface.set_colorkey(0)
        if FixedTextbox:
            _class = TextBox(surface,pygame.Surface((box[0],box[1])))
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
    
class Button():
    def __init__(self,pos,size,colour,icon,scale,func=None,arg=None):
        UpScaledSize = (size[0]*scale,size[1]*scale)
        self.rect = pygame.Rect((0,0),UpScaledSize)
        self.rect.center = (pos[0],pos[1])

        self.bimage = pygame.Surface(UpScaledSize)
        self.bimage.fill(colour)
        self.bimage.blit(icon,(UpScaledSize[0]/2 - icon.get_width()/2,UpScaledSize[1]/2 - icon.get_height()/2))

        self.func = func
        self.down = False
        self.hovered = False
        self.selected = False

        self.dark = pygame.Surface(UpScaledSize,pygame.SRCALPHA)
        self.dark.fill((0,0,0,100))
        self.mask = pygame.mask.from_surface(self.bimage)
        self.outline =  [coord for coord in self.mask.outline(4)]

        self.type = 'button'
        self.arg = arg

    def update(self,events,mouse,game=None):
        hover = False
        if self.rect.collidepoint(mouse):
            hover = True
        if hover == False:
            self.down = False
            self.hovered = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and hover:
                self.down = True
                self.hovered= True
                self.selected = True
            if event.type== pygame.MOUSEBUTTONUP and event.button == 1 and self.hovered == True and hover:
                if self.arg != None:
                    self.func(game,self.arg)
                elif self.func:
                    self.func(game)
                
                self.selected = False
                self.hovered = False
                self.down = False
            elif  event.type== pygame.MOUSEBUTTONUP and event.button == 1:
                self.selected = False

        if self.down:
            self.image = self.bimage.copy()
            self.image.blit(self.dark,(0,0))
        else:
            self.image = self.bimage.copy()

        if hover or self.selected:
            pygame.draw.polygon(self.image,(255,255,255),self.outline,4)

    def collidepoint(self,point):
        if self.rect.collidepoint(point):
            return True
        else:
            return False

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class Slider():
    def __init__(self,pos,size,colour,_scale,padding=1,value=[1,2],default=1) -> None:
        #sizing
        pos = scale(_scale,pos)
        size = scale(_scale,size)
        self.scale = _scale
        self.padding = padding
        self.type = 'slider'

        #colours
        self.colour = colour[0]
        self.accent = colour[1]
        self.barColour = colour[2]

        #rect
        self.rect  = pygame.Rect(pos,size)
        self.bar = pygame.Rect((vec(pos)+(padding*_scale,padding*_scale)),(vec(size)-(padding*2*_scale,padding*2*_scale)))

        #selection
        self.baractive = False
        self.range = max(value) - (min(value)-1)
        self.values = value
        if self.range > 1:
            self.increment = self.bar.width / (self.range - 1)
        self.offset = (default -min(self.values)) * self.increment
        self.current = default
        self.barvalue = default  

        #image
        self.bimage = pygame.Surface(size)
        self.bimage.fill(self.colour)
        pygame.draw.rect(self.bimage,self.accent,((padding*_scale,padding*_scale),self.bar.size))
        self.mask = pygame.mask.from_surface(self.bimage)
        self.outline =  [coord for coord in self.mask.outline(2)]
        self.image = self.bimage.copy()
        pygame.draw.rect(self.image,self.barColour,((self.padding*self.scale,self.padding*self.scale),(self.offset,self.bar.height)))

    def update(self,events,mouse,game):
        self.bar.topleft = vec(self.rect.topleft)+(self.padding*self.scale,self.padding*self.scale)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
                if self.rect.collidepoint(mouse):
                    self.baractive = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.barvalue = self.current

        if self.baractive:
            self.offset = vec(mouse).x - self.bar.topleft[0]
            if self.offset < 0:
                self.offset = 0
            elif self.offset > self.bar.width:
                self.offset = self.bar.width

        #getting the value from the bar
        
            fullness = self.offset / self.increment #how many values it is along the slider
            number = round(fullness) #round to int
            self.current = min(self.values) + number
            
        
        if not mouse_buttons()[0]:
            self.baractive = False

        if self.rect.collidepoint(mouse):
            self.image = self.bimage.copy()
            pygame.draw.rect(self.image,self.barColour,((self.padding*self.scale,self.padding*self.scale),(self.offset,self.bar.height)))
            self.drawoutline()
            amount = game.text.render(f'gui scale:{self.current}',1).image
            self.image.blit(amount,(self.rect.width/2-amount.get_width()/2,self.rect.height/2-amount.get_height()/2))
        else:
            self.image = self.bimage.copy()
            pygame.draw.rect(self.image,self.barColour,((self.padding*self.scale,self.padding*self.scale),(self.offset,self.bar.height)))
            amount = game.text.render(f'gui scale:{self.current}',1).image
            self.image.blit(amount,(self.rect.width/2-amount.get_width()/2,self.rect.height/2-amount.get_height()/2))

    def drawoutline(self):
        pygame.draw.lines(self.image,'white',True,self.outline)

    def draw(self,screen):
        screen.blit(self.image,self.rect)

#can make vertical and horizontal columns
class Column():
    def __init__(self,pos,spacing,scale,direction,name=None, elements = None):
        self.pos = pos
        self.direction = direction
        self.elements = []
        self.dictionary = None
        self.type = 'column'
        self.spacing = spacing * scale
        self.name = name
        self.height = 0
        self.width = 0

        self.rect = pygame.Rect(0,0,1,1)
        self.rect.center = self.pos

        if elements != None:
            self.AddElement(elements)

    def AddElement(self,elements=None): 
        if type(elements) == list:
            for item in elements:
                self.elements.append(item)
        elif type(elements) == dict:
            for item in list(elements.values()):
                self.elements.append(item)
            self.dictionary = elements
        elif hasattr(elements,'__dict__'):
            self.elements.append(elements)

        #column
        if self.direction == 'vertical':
            self.height = 0
            self.pos = self.rect.center
            self.width = max(map(lambda x: x.rect.width,self.elements))
            for item in self.elements:
                item.rect.center = vec(0,self.height+item.rect.height/2)
                self.height += item.rect.height
                self.height += self.spacing
            self.height -= self.spacing
            direction = vec(self.pos[0],self.pos[1] - self.height/2)
            for item in self.elements:
                item.rect = item.rect.move(direction)
                
            self.rect = pygame.Rect(0,0,self.width,self.height); self.rect.center = self.pos
        #row
        elif self.direction == 'horizontal':
            self.pos = self.rect.center
            self.width = 0
            self.height = max(map(lambda x: x.rect.height,self.elements))
            for item in self.elements:
                item.rect.center = vec(self.width+item.rect.width/2,0)
                self.width += item.rect.width
                self.width += self.spacing
            self.width -= self.spacing
            direction = vec(self.pos[0] - self.width/2,self.pos[1])
            for item in self.elements:
                item.rect = item.rect.move(direction)
            self.rect = pygame.Rect(0,0,self.width,self.height); self.rect.center = self.pos

    def collidepoint(self,point):
        for item in self.elements:
            if item.collidepoint(point):
                return True
            else:
                return False

    def update(self,events, mouse, game= None):
        for item in self.elements:
            item.update(events,mouse,game)

    def draw(self,screen):
        for item in self.elements:
            item.draw(screen)

#gridiigidiy gridding :)
class Grid():
    def __init__(self,center,spacing,scale,text,size,structure,name=None,elements=None) -> None:
        self.center = vec(center)
        self.unscaledSpacing = spacing
        self.spacing = spacing * scale
        self.scale = scale
        self.text = text
        self.type = 'grid'
        self.size = vec(size) * scale
        self.name = name
        self.structure = structure
        self.elements = []
        self.pages = {}
        self.activegroup = None
        self.dictionary = {}
        #add elements
        if elements != None:
            self.createPages(elements)

    def createPages(self,elements=None):
        self.addelements(elements)
        arrowSize = 18
        self.maxwidth = self.size[0]-(self.spacing * 4 + arrowSize*self.scale*2)

        if self.maxwidth < 1 : print('grid width to small')

        if self.structure == 'variable':
            self.makeVarColumns()
        elif self.structure == 'fixed':
            self.makeFixedGrids()

        #setgroup to active
        self.activegroup = self.pages['0']
        #create arrow buttons
        self.createArrows(arrowSize)
        
    def makeVarColumns(self):    
        self.rows = []
        self.width = -self.spacing
        self.height = -self.spacing
        self.thisrow = []
        #put all the elements into columns that fit horizontally or rows
        for item in self.elements:
            self.width += item.rect.width + self.spacing
            if self.width > self.maxwidth:
                self.addColumn()
                self.thisrow.append(item)
                self.width += item.rect.width + self.spacing
            else:
                self.thisrow.append(item)
        if self.thisrow:
            self.addColumn()
        #put all rows into pages that fit the right amount
        self.thiscolumn = []
        page = 0
        for row in self.rows:
            self.height += item.rect.height + self.spacing
            if self.height > self.size[1]:
                self.genPageVar(page)
                page += 1
                self.thiscolumn.append(row)
                self.height += item.rect.height + self.spacing
            else:
                self.thiscolumn.append(row)
        if self.thiscolumn:
            self.genPageVar(page)
    
    def addColumn(self):
        newcolumn = Column((0,0),self.unscaledSpacing,self.scale,'horizontal','row',self.thisrow)
        self.thisrow = []
        self.width = -self.spacing
        self.rows.append(newcolumn)
        
    def addelements(self,elements=None):
        if type(elements) == list:
            for item in elements:
                self.elements.append(item)
        elif type(elements) == dict:
            for item in list(elements.values()):
                self.elements.append(item)
            self.dictionary = elements
        elif hasattr(elements,'__dict__'):
            self.elements.append(elements)

    def makeFixedGrids(self):
        buttonSize = self.elements[0].rect.size
        #amount of elements across and down
        gridwidth = self.getGridWidth(buttonSize)
        gridheight = self.getGridHeight(buttonSize)
        gridsize = (gridwidth,gridheight)
        #grabbing outside edge size of the grid in pixels
        width = buttonSize[0] * gridwidth + self.spacing*(gridwidth-1)
        height = buttonSize[1] * gridheight + self.spacing*(gridheight-1)
        size = (width,height)
        #splitting elements into grid area sized lists
        paged = self.splitElements(gridwidth * gridheight)
        #assign all elements grid postions
        paged = self.assignPos(size, gridsize,buttonSize, paged)
        #put all the elements into pages:
        self.genPageFixed(paged)

    def genPageFixed(self, paged):
        for index,i in enumerate(paged):
            container = UiContainter(f'page {index}')
            container.AddElement(i)
            self.pages[str(index)] = container
        
    def assignPos(self,size, gridsize,buttonSize,paged):
        getgrid = lambda index : (index % gridsize[0],index // gridsize[0])
        for page in paged:
            for index,i in enumerate(page):
                gridpos = getgrid(index)
                
                i.rect.center = ((self.center[0]-(size[0]/2)) + buttonSize[0]/2 + (gridpos[0] * (buttonSize[0]+self.spacing)),self.center[1]-size[1]/2 + buttonSize[1]/2 + (gridpos[1] * (buttonSize[1]+self.spacing)))

        return paged

    def splitElements(self, length):
        paged = []
        buffer = []
        for i in self.elements:
            buffer.append(i)
            if len(buffer) == length:
                paged.append(buffer)
                buffer = []
        if buffer:
            paged.append(buffer)
        
        return paged

    def getGridWidth(self,buttonSize):
        width = -self.spacing
        count = 0
        while True:
            width += buttonSize[0] + self.spacing
            if width > self.maxwidth:
                break
            count +=1
        
        return count

    def getGridHeight(self,buttonSize):
        height = -self.spacing
        count = 0
        while True:
            height += buttonSize[1] + self.spacing
            if height > self.size[1]:
                break
            count +=1
        
        return count

    def genPageVar(self,index):
        grid = Column(self.center,self.unscaledSpacing,self.scale,'vertical','grid',self.thiscolumn)
        for element in grid.elements:
            element.AddElement()
        container = UiContainter(f'page {index}')
        container.AddElement(grid)
        self.height = -self.spacing
        self.thiscolumn = []
        self.pages[str(index)] = container

    def createArrows(self,arrowSize):
        for key in self.pages:
            if key == '0' and len(list(self.pages.values()))>1:
                rightbutton = Button(vec(self.center.x + self.maxwidth/2 + self.spacing + arrowSize*self.scale/2,self.center[1]),(arrowSize,arrowSize),(0,100,200),self.text.render('>',2,False).image,self.scale,self.changeActive,'1')
                self.pages[key].AddElement(rightbutton)
            elif key == str(len(list(self.pages.values()))-1) and len(list(self.pages.values()))>1:
                leftbutton = Button(vec(self.center.x - self.maxwidth/2 - self.spacing - arrowSize*self.scale/2,self.center[1]),(arrowSize,arrowSize),(0,100,200),self.text.render('<',2,False).image,self.scale,self.changeActive,str(int(key)-1))
                self.pages[key].AddElement(leftbutton)
            elif len(list(self.pages.values()))>1:
                ikey = int(key)
                rightbutton = Button(vec(self.center.x + self.maxwidth/2 + self.spacing + arrowSize*self.scale/2,self.center[1]),(arrowSize,arrowSize),(0,100,200),self.text.render('>',2,False).image,self.scale,self.changeActive,str(ikey +1))
                leftbutton = Button(vec(self.center.x - self.maxwidth/2 - self.spacing - arrowSize*self.scale/2,self.center[1]),(arrowSize,arrowSize),(0,100,200),self.text.render('<',2,False).image,self.scale,self.changeActive,str(ikey-1))
                self.pages[key].AddElement([leftbutton,rightbutton])

    def changeActive(self,game,key):
        self.activegroup = self.pages[key]
        self.activegroup.update(game.events,game.mouse,game)

    def update(self,events,mouse,game=None):
        self.activegroup.update(events,mouse,game)

    def draw(self,screen):
        self.activegroup.draw(screen)

    def collidepoint(self,point):
        self.activegroup.collidepoint(point)

class UiContainter():
    def __init__(self,name=None, elements=None):
        self.elements = []
        self.name = name
        self.dictionary = None
        self.type = 'container'
        self.AddElement(elements)

    def AddElement(self,elements=None):
        if type(elements) == list:
            for item in elements:
                self.elements.append(item)
        elif type(elements) == dict:
            for item in list(elements.values()):
                self.elements.append(item)
            self.dictionary = elements
        elif hasattr(elements,'__dict__'):
            self.elements.append(elements)
    
    def update(self,events, mouse, game=None):
        for item in self.elements:
            item.update(events,mouse,game)
    
    def collidepoint(self,point):
        for item in self.elements:
            if item.collidepoint(point):
                return True
            else:
                return False

    def draw(self,screen):
        for item in self.elements:
            item.draw(screen)




            

