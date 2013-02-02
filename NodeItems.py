# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import os
import platform

SCREENWIDTH = 800
SCREENHEIGHT = 600
TEXTRECTHEIGHT = 160
LINENUMBER = 35 
## collect all narrow char...you can add it
CHAR = u'''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-=[]:;{}+_,.?!()@<>""''/\\'''
OFFY = 10
OFFX = 35
VSIZE = 30
ALPHA = 180
CHOICEBUTTONFROMTOP = 50
CHOICEBUTTONSIZE = (200,40)

if platform.system() == 'Windows':
	WINDOWS = 1
else:
        WINDOWS = 0

class Button(object):
    ##As a Button,these properties are necessary:
    ##A RECT:Contains the pos and size
    ##THE label:A micro text
    ##THE Image:decide the LOOK of the button
    def __init__(self,pos,size,image,font,label = '',bgcolor = None,fontSize = 24):
        self.pos = pos
        self.size = size
        self.surface = pygame.Surface(size,SRCALPHA)
        if WINDOWS:
                self.label = label.decode('gb18030')
        else:
                self.label = label.decode('utf8')
        self.fontColor = (0xFF,0xFF,0xFF)

        ##To make sure the function is'n too long
        ##I split the code to three functions
        self.image = self.__LoadImage(image,bgcolor)
        self.font = self.__LoadFont(font,fontSize) 
        self.__Combination()


    def __LoadImage(self,image,bgcolor):
        ## Use the pure color
        if bgcolor != None:
            try:
                self.surface.fill(bgcolor)
            except pygame.error:
                print 'Cannot use the color'
                raise SystemExit
            return self.surface
        ## Use a image
        else:
            try:
                Image = pygame.image.load(image).convert_alpha()
            except pygame.error:
                print 'Could not load the image'
                raise SystemExit
            Image = pygame.transform.scale(Image,self.size)
            return Image

    ##Maybe I should consider reuse the code
    ##Now It is stupid
    def __LoadFont(self,font,fontSize):
        try:
            font = pygame.font.Font(font,fontSize)
        except pygame.error,message:
            print 'Cannot load font:',name
            raise SystemExit,message
        return font

    def __Combination(self):
        Image = self.image
        labelSurface = self.font.render(self.label,True,self.fontColor)
        xPos = (Image.get_width() - labelSurface.get_width())/2
        yPos = (Image.get_height() - labelSurface.get_height())/2
        Image.blit(labelSurface,(xPos,yPos))
        self.surface.blit(Image,(0,0))

    def render(self,surface):
        x,y = self.pos
        w,h = self.surface.get_size()
        x -= w/2
        y -= h/2
        surface.blit(self.surface,(x,y))

    ## check one point is in THIS BUTTON
    ## Orz,repeat codes....I'm lazy...
    def is_over(self,point):
        x,y = self.pos
        w,h = self.surface.get_size()
        x -= w/2
        y -= h/2
        rect = pygame.Rect((x,y),self.size)
        return rect.collidepoint(point)

    def get_pos(self):
        return self.pos
    
    def get_surface(self):
        return self.surface

    def get_rect(self):
        return self.surface.get_rect()


class NodeItem(object):
    '''The Main class,contain the basic
    Items of each frame,I try to make it
    simply but I found it too difficult.
    The basic items,contains:
        The background
        The BGM
        The Text
        Maybe The Portrait(s)
        '''
    def __init__(self,surface):
                
        self.BGM = ''
        self.Index = 0
        self.NextIndex = 0

        self.BGName = ''
        self.BGMName = ''
        self.BGChange = 0
        self.ChoiceButtons = {}
        self.Portraits = {}

        self.bgColor = ((0x00,0x00,0x00))
        self.fgColor = ((0xFF,0xFF,0xFF))
        self.TextBoxPos = (0,SCREENHEIGHT-TEXTRECTHEIGHT)

        self.Surface = surface
        self.Font = self.__initFont()
        self.TextBox , self.TextBoxRect = self.__initTextRect()
        self.__updateImage('ErrorIndex.jpg')


    def __initTextRect(self,colorkey = ALPHA):
        size = (SCREENWIDTH,TEXTRECTHEIGHT)
        TextRect = pygame.Surface(size)
        TextRect.fill(self.bgColor) ##which is the dialogueBox's Color
        if colorkey is not None:
          ##  if colorkey is -1:
           ##     colorkey = TextRect.get_at((0,0))
          ##  TextRect.set_colorkey(colorkey, RLEACCEL)
            TextRect.set_alpha(colorkey)
        return TextRect , TextRect.get_rect()

    def __initFont(self,name = 'hksn.ttf',size = 20):
        fullname = os.path.join('FONT',name)
        try:
            font = pygame.font.Font(fullname,size)
        except pygame.error,message:
            print 'Cannot load font:',name
            raise SystemExit,message
        return font

    ## render all items on screen.
    def update(self,parser):
        self.__updateNodeIndex(parser.getNodeIndex())
        self.__updateBGM(parser.getBGM())
        self.Background = self.__updateImage(parser.getBackground())
        self.__updateText(parser.getName(),parser.getText())
        
        self.__updatePortrait(parser.getPortrait())

        
        ## blit background
        self.Surface.blit(self.Background,(0,0))

        ## Portraits----always are complex
        ## blit portraits
        if self.Portraits:
            for key in self.Portraits:
                try:
                    name = self.Portraits[key]['name']
                    clip_pos = self.Portraits[key]['clip_pos']
                    size = self.Portraits[key]['size']
                    screen_pos = self.Portraits[key]['screen_pos']
                except KeyError:
                    print 'The portraits argvs are not enough in %d' % self.Index
                    raise SystemExit
                else:
                    portrait = self.__updateImage(name,-1,clip_pos,size)
                   ## x = (SCREENWIDTH - size[0] + screen_pos[0])/2
                   ## y = (SCREENHEIGHT - size[1] +  screen_pos[1])/2
                    x , y = screen_pos
                    x -= size[0]/2
                    y -= size[1]/2
                    self.Surface.blit(portrait,(x,y))

        ## blit textbox
        self.Surface.blit(self.TextBox,self.TextBoxPos)

        ## blit choice buttons
        if parser.getChoice() != []:
            self.__updateChoice(parser.getChoice())
            for i in self.ChoiceButtons.keys():
                self.ChoiceButtons[i][1].render(self.Surface)
        else:
            self.ChoiceButtons = {}
        
            ##Where is only for test



    def __updateNodeIndex(self,index):
        self.Index = index
        
    ## This time will extend the function
    ## which supported background and portrait
    def __updateImage(self,name,colorkey=None,clip_pos = None,size = None):
        if clip_pos and size :
            fullname = os.path.join('PORTRAIT',name)
        elif not clip_pos and not size:
            fullname = os.path.join('BG',name)
        else:
            raise SystemExit,message
        try:
            image = pygame.image.load(fullname)
        except pygame.error,message:
            print 'Cannot load image:',name
            raise SystemExit, message
        image = image.convert()
        if clip_pos:
            image = image.subsurface((0,0),clip_pos)
        if size:
            image = pygame.transform.scale(image,size)
        else:
            image = pygame.transform.scale(image,(SCREENWIDTH,SCREENHEIGHT))
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image

        ## portraits is a dict of dict
        ## like this:
        ## {'backgound.jpg': {'clip_pos': (100, 100), 'screen_pos': (212, 54), 'name': 'aa.jpg', 'size': (121, 44)}, 'gg.jpg': {'clip_pos': (100, 100), 'screen_pos': (212, 54), 'name': 'aa.jpg', 'size': (121, 44)}, 'aa.jpg': {'clip_pos': (100, 100), 'screen_pos': (212, 54), 'name': 'aa.jpg', 'size': (121, 44)}}
        ## So complex,I know.....
        ## handle self.Portraits

    def __updatePortrait(self,portraits):
        if portraits == {}:
            self.Portraits = {}
        else:
            ## update self.Portraits
            for key in portraits:
                if key not in self.Portraits:
                    temp_dict = {}
                    temp_dict[key] = portraits[key]
                    self.Portraits.update(temp_dict)
                else:
                    for sec_key in portraits[key]:
                        self.Portraits[key][sec_key] = portraits[key][sec_key]
            ## delete items which isn't contained portraitz
                ## list production can't apply the exceptions
                ##delete_key = [i for i in self.Portraits.keys() if self.Portraits[i]['flag']]
            delete_key_list = []
            for i in self.Portraits.keys():
                try:
                    if self.Portraits[i]['flag']:
                        delete_key_list.append(i)
                except KeyError:
                    pass
            for i in delete_key_list:
                self.Portraits.pop(i)



                    


    def __updateBGM(self,name):
        class NoneSound:
            def play(self):pass
        if not pygame.mixer:
            return NoneSound()
        fullname = os.path.join('BGM',name)
        if self.BGMName == fullname:
            return 
        try:
            pygame.mixer.music.load(fullname)
        except pygame.error, message:
            print 'Cannot load sound:',fullname
            raise SystemExit,message
        self.BGMName = fullname
        self.play()
     
    def play(self):
        pygame.mixer.music.play(-1,0.0)

    def stop(self):
        pygame.mixer.music.stop()       
        
    def __updateChoice(self,choice_branch):
        dir_button = {}
        num_choice = len(choice_branch)
        button_distance = (SCREENHEIGHT-2*CHOICEBUTTONFROMTOP)/(1+num_choice)
        for (count,i) in enumerate(choice_branch):
            dir_button[i[0]] = (i[1],Button(\
            (SCREENWIDTH/2,CHOICEBUTTONFROMTOP+button_distance*(1+count)),\
            CHOICEBUTTONSIZE,'button.png',os.path.join('FONT','hksn.ttf'),\
            i[0]))
        
        self.ChoiceButtons = dir_button

    ## use the function to align lines.In face,the function is ugly...
    def textToList(self,text):
        width = 0
        textList = []
        textStr = ''
        for i in text:
            if i in CHAR or i.isdigit() or i.isspace():
                width += 1
            else:
                width += 2
            textStr += i
            if width >= LINENUMBER * 2 - 1:
                textList.append(textStr)
                textStr = ''
                width = 0
        textList.append(textStr)
        return textList
        
    def __updateText(self,name,text):
        self.TextBox.fill(self.bgColor)
        if WINDOWS:
                name = name.decode('gb18030')
                text = text.decode('gb18030')
        else:
                name = name.decode('utf8')
                text = text.decode('utf8')
        ##textLines = [text[i:i+LINENUMBER] for i in range(len(text)) if i % LINENUMBER == 0]
        textLines = self.textToList(text)
        if name != '':
            name += ' :'
        textLines.insert(0,name)
       ## vSize = TEXTRECTHEIGHT / len(textLines)
        vSize = VSIZE

        for lineNum in range(len(textLines)):
            currentLine = textLines[lineNum]
            fontSurface = self.Font.render(currentLine,True,self.fgColor,self.bgColor)
            ##xPos = (SCREENWIDTH- fontSurface.get_width())/2
            xPos = OFFX
            yPos = OFFY + lineNum * vSize
            self.TextBox.blit(fontSurface,(xPos,yPos))

    def getNextIndex(self):
        return self.NextIndex

    def setNextIndex(self,index = -1):
        if index == -1:
            self.NextIndex = self.Index + 1
        else:
            self.NextIndex = index

    def getChoiceButtons(self):
        return self.ChoiceButtons

