import pygame,math
from pygame.math import Vector2 as vec
from pygame.mouse import get_pressed as mouse_buttons
from .utils import *

class Word_Image():
    def __init__(self,image,positions):
        self.image = image
        self.positions = positions
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
        self.scale = scale
        self.spacing = spacing
        #getting letters from spprite sheet
        self.cutLetters(image)
        self.space = self.letters[' '].get_width() + self.spacing
    
    def cutLetters(self, image):
        self.letters = {}
        self.letLengths = {}
        count = 0
        order = " abcdefghijklmnopqrstuvwxyz,'.:-?!1234567890/\()[]<>"
        self.lstart = None
        for pixel in range(image.get_width()):
            p = image.get_at((pixel,0))
            if self.lstart != None and p == (255,0,0):
                #get image letter
                dist = pixel - self.lstart -1
                height = image.get_height()
                pos= (self.lstart+1,0)
                #cutting
                letter = self.get_letter(image,pos,(dist,height))
                #adding to dictionary
                self.letters[order[count]] = letter
                count +=1
            if p == (255,0,0):
                self.lstart = pixel
        
        for key in self.letters:
            self.letLengths[key] = self.letters[key].get_width()
    
    def get_letter(self, image, pos, size):
        letter = image.subsurface((pos,size))
        letter.set_colorkey((0,0,0))
        return letter

    def render(self, text, fontSize, clr=None, width=0):
        self.size = self.scale * fontSize
        self.width = width * self.scale
        self.split_text = self.splitText(str(text))
        #making a dictionary that holds the scaled size of each letter
        self.sizedLetLengths = {}
        for key in self.letLengths:
            self.sizedLetLengths[key] = self.letLengths[key] * self.size
        #writes all text into self.lines
        self.writeLines()
        #getting topright of every letter
        self.positions = self.returnPos()
        #returning all lines with newline characters on so 
        #drawing
        surface = self.drawLines()
        #pallete swap if necessary
        if clr:
            surface = self.swap_pallet(surface, clr)

        return Word_Image(surface,self.positions)

    def returnPos(self):
        positions = []
        for y,line in enumerate(self.lines):
            x_offset = self.spacing*self.size
            linePos = []
            for letter in line:
                x_offset += self.sizedLetLengths[letter]
                pos = (x_offset,y*self.size*self.letters[' '].get_height())
                x_offset += self.spacing*self.size
                data = (letter,pos)
                linePos.append(data)
            positions.append(linePos)
        return positions

    def drawLines(self):
        if self.width == 0:
            maxwidth = max([self.getLength(line) for line in self.lines])
            #if width is unspecified do it to the largest line width
            surface = pygame.Surface((maxwidth,self.letters[' '].get_height()*self.size*len(self.lines)))
        else:
            surface = pygame.Surface((self.width,self.letters[' '].get_height()*self.size*len(self.lines)))
        #blitting
        scaleLetters = {}
        for key in self.letters:
            scaleLetters[key] = pygame.transform.scale(self.letters[key],(self.sizedLetLengths[key],self.letters[key].get_height()*self.size))
        for y,line in enumerate(self.lines):
            x_offset = self.spacing *self.size
            for letter in line:
                surface.blit(scaleLetters[letter],(x_offset,y*scaleLetters[' '].get_height()))
                x_offset += self.sizedLetLengths[letter] + self.spacing * self.size
        surface.set_colorkey((0,0,0))

        return surface

    def writeLines(self):
        self.lines = []
        self.line = ''
        self.lineWidth = self.spacing*self.size
        for word in self.split_text:
            if word[0] == '\n':
                #newline character
                self.lines.append(self.line)
                self.lineWidth = self.spacing*self.size
                self.line = ''
            elif self.width == 0:
                if not self.line:
                    self.line += word[0]
                else:
                    self.line += ' ' + word[0]
            elif self.width > 0 and word[1] > self.width:
                #when word is too big of a line it chops it
                if self.line:
                    self.lines.append(self.line)
                self.lineWidth = self.spacing*self.size
                self.splitWord(word)
            elif self.width > 0 and self.lineWidth < self.width:
                self.addWord(word)
        if self.line:
            self.lines.append(self.line)

    def addWord(self,word):
        #only add space if word before it
        if not self.line:
            wordWidth = word[1]
        else:
            wordWidth = self.space * self.size + word[1]
        testWidth = self.lineWidth + wordWidth
        #checking to make sure there is enought space
        if testWidth <= self.width:
            if not self.line:
                self.line += word[0]
            else:
                self.line += ' ' + word[0]
            lineWidth += wordWidth
            if lineWidth == self.width:
                #If the same next line cos no more will fit
                self.lines.append(self.line)
                self.lineWidth = self.spacing*self.size
                self.line = ''
        else:
            #if testwidth goes over, new line and add word to it
            self.lines.append(self.line)
            self.lineWidth = self.spacing*self.size + word[1]
            self.line = word[0]

    def splitWord(self,word):
        self.line = ''
        self.lineWidth = 0
        for letter in word[0]:
            if letter != '\n':
                testWidth = self.lineWidth + self.spacing * self.size + self.sizedLetLengths[letter]
                #making sure it doesnt exceed width or is only one character
                if testWidth <= self.width or len(self.line) == 0:
                    self.line += letter
                    self.lineWidth += self.spacing * self.size + self.sizedLetLengths[letter]
                    if self.lineWidth == self.width:
                        self.lines.append(self.line)
                        self.line = ''
                        self.lineWidth = self.spacing*self.size
            #resetting line
            if letter == '\n' or testWidth > self.width:
                self.lines.append(self.line)
                self.line = letter
                self.lineWidth = self.spacing*self.size + self.sizedLetLengths[letter] + self.spacing * self.size

    def splitText(self,text):
        words = text.split('\n')
        words = ' \n '.join(words)
        words = words.split(' ')
        split_text = [[word,self.getLength(word)] for word in words]

        return split_text

    def getLength(self,word):
        if word != "\n":
            width = 0
            for letter in word:
                width += self.letters[letter].get_width() * self.size + self.spacing * self.size
        elif word == "\n":
            width = 0
        
        return width

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
        self.image = self.bimage.copy()

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
    def __init__(self,pos,size,colour,_scale,padding=1,value=[1,2],func = None,default=1) -> None:
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
        self.func = func
        self.baractive = False
        self.range = max(value) - (min(value)-1)
        self.values = value
        if self.range > 1:
            self.increment = self.bar.width / (self.range - 1)
        else:
            self.increment = 1
        self.offset = (default -min(self.values)) * self.increment
        self.current = default 

        #image
        if self.range > 1:
            self.barsize = self.increment * (self.current - 1)
        else:
            self.barsize = self.bar.width
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
                self.baractive = False
                if self.func:
                    self.func(game, self.current)

        if self.baractive:
            self.offset = vec(mouse).x - self.bar.topleft[0]
            if self.offset < 0:
                self.offset = 0
            elif self.offset > self.bar.width:
                self.offset = self.bar.width

        #getting the value from the bar
        
            fullness = self.offset / self.increment #how many values it is along the slider
            number = round(fullness) #round to int
            if self.range > 1:
                self.current = min(self.values) + number
            else:
                self.current = 1
        
            if self.range > 1:
                self.barsize = self.increment * (number)
            else:
                self.barsize = self.bar.width

        if self.rect.collidepoint(mouse):
            self.image = self.bimage.copy()
            pygame.draw.rect(self.image,self.barColour,((self.padding*self.scale,self.padding*self.scale),(self.barsize,self.bar.height)))
            self.drawoutline()
            amount = game.text.render(f'gui scale:{self.current}',1).image
            self.image.blit(amount,(self.rect.width/2-amount.get_width()/2,self.rect.height/2-amount.get_height()/2))
        else:
            self.image = self.bimage.copy()
            pygame.draw.rect(self.image,self.barColour,((self.padding*self.scale,self.padding*self.scale),(self.barsize,self.bar.height)))
            amount = game.text.render(f'gui scale:{self.current}',1).image
            self.image.blit(amount,(self.rect.width/2-amount.get_width()/2,self.rect.height/2-amount.get_height()/2))

    def drawoutline(self):
        pygame.draw.lines(self.image,'white',True,self.outline)

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class UiContainter():
    def __init__(self,name=None, elements=None):
        self.elements = []
        self.name = name
        self.dictionary = {}
        self.type = 'container'
        self.AddElement(elements)

    def fillElements(self):
        self.elements = []
        for key in self.dictionary:
            self.elements.append(self.dictionary[key])

    def removeItem(self, name):
        del self.dictionary[name]
        self.fillElements()

    def AddElement(self,elements=None):
        if type(elements) == list:
            for item in elements:
                self.elements.append(item)
        elif type(elements) == dict:
            self.dictionary.update(elements)
            self.fillElements()
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

#can make vertical and horizontal columns
class Column(UiContainter):
    def __init__(self,pos,spacing,scale,direction,name=None, elements = None):
        self.pos = pos
        self.direction = direction
        self.elements = []
        self.dictionary = {}
        self.type = 'column'
        self.spacing = spacing * scale
        self.name = name
        self.height = 0
        self.width = 0

        self.rect = pygame.Rect(0,0,1,1)
        self.rect.center = self.pos

        if elements != None:
            self.createColumn(elements)

    def centerElements(self):
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

    def createColumn(self,elements=None): 
        self.AddElement(elements)
        
        self.centerElements()

    def update(self,events, mouse, game= None):
        for item in self.elements:
            item.update(events,mouse,game)

    def draw(self,screen):
        for item in self.elements:
            item.draw(screen)

#gridiigidiy gridding :)
class Grid(UiContainter):
    def __init__(self,center,spacing,guiscale,scale,text,size,structure,name=None,elements=None) -> None:
        self.center = vec(center)
        self.unscaledSpacing = spacing
        self.spacing = spacing * guiscale
        self.scale = guiscale
        self.text = text
        self.type = 'grid'
        self.size = vec(size) * scale
        self.name = name
        self.structure = structure
        self.elements = []
        self.pages = {'0':UiContainter('page 0')}
        self.activegroup = None
        self.dictionary = {}
        #add elements
        if elements != None:
            self.createPages(elements)

    def removeItem(self, name):
        del self.dictionary[name]
        self.pages = {'0':UiContainter('page 0')}
        self.fillElements()
        self.createPages()

    def createPages(self,elements=None):
        self.AddElement(elements)
        if self.elements:
            arrowSize = 18
            self.maxwidth = self.size[0]-(self.spacing * 4 + arrowSize*self.scale*2)

            if self.maxwidth < 1 : print('grid width to small')

            if self.structure == 'variable':
                self.makeVarColumns()
            elif self.structure == 'fixed':
                self.makeFixedGrids()
        else:
            self.pages = {'0':UiContainter('page 0')}
        #setgroup to active
        self.activegroup = self.pages['0']
        #create arrow buttons
        if self.elements:
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
            element.centerElements()
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





            

