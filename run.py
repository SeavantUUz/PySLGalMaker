# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from sys import exit
import NodeItems
import Parser
import os
import pickle

ERRORINDEX = 65535
SIZE = (NodeItems.SCREENWIDTH,NodeItems.SCREENHEIGHT)
EXIT_POS = (70,530)
EXIT_SIZE = (150,150)

pygame.init()
screen = pygame.display.set_mode((800,600),0,32)
clock = pygame.time.Clock()

parser = Parser.Parser()
LNode = parser.split('script.sanae')
dirNode = {}
for i in LNode:
    dirNode[parser.searchIndex(i)] = i

    
## Create an instance of the NodeItem
## which contains the musics,images,and
## text,buttons etc.
## In face,One NodeItem represents a
## frame which you are watching
freeze = False
g_flag = ''
now_frame = ''
save_image = 'tmp.png'
load_data = None
## which to parser save data
## reuse the class
save_parser = Parser.Parser()
nodeItem = NodeItems.NodeItem(screen)
dict_settingButtons = nodeItem.getSettingButtons()
parser.parser(dirNode[0])
nodeItem.update(parser)

def savefile_parser():
    fullname = os.path.join('SAVE','save.dat')
    saveInfo = save_parser.split(fullname)
    saveInfos = []
    ##saveInfos = [save_parser.parser(i).getSaveData() for i in saveInfo]
    try:
        for i in saveInfo:
            save_parser.parser(i)
            saveInfos.append(save_parser.getSaveData(i))
        ## i->like this:(0,'xxx.jpg,25)
        ## saveSurfaces composed like this:
        ## [(0,<xxxxxxsurfacexxxx>),(1,<xxx>...)]
        saveSurfaces = [(i[0],pygame.transform.scale(pygame.image.load(os.path.join('SAVE',i[1])).convert(),(200,200))) for i in saveInfos]
        dict_item = {}
        dict_name = {}
        for i in saveSurfaces:
            ## dict_item's value is an
            ## instance of Surface class
            dict_item[i[0]] = i[1]
        for i in saveInfos:
            ## dict_name is a dict
            ## like this {0:('xxx.jpg',25,xxxxxxxx)}
            dict_name[i[0]] = (i[1],i[2])
    except AttributeError:
        dict_item = {}
        dict_name = {}
    return (dict_item,dict_name)

def format_save_data(saveDict,savefile):
    return '\n\n'.join([str(i[0])+'\n'+'''[background='''+"'"+ \
            str(i[1][0])+"']" + '\n' \
            + str(i[1][1])
            for i in saveDict.items()])
    ##return '\n\n'.join([str(i[0])+'\n' + '''[backgroud='''+"'"+ \
    ##        str(i[1][0])+"']" + '\n' + str(i[1][1]) \
    ##        for i in saveDict.items()])

def button_settings(surface,pos,Frame,flag=''):
    global freeze
    global g_flag
    global now_frame
    global load_data
    ##save_image_surface = pygame.image.load(save_image).convert()
    ##save_image_surface = pygame.transform.scale(save_image_surface,(200,200))
    ## need updating?
    if flag:
        now_frame = surface.copy() 
        now_frame = pygame.transform.scale(now_frame,(200,200))
        g_flag = flag

    ## init the setting screen
    fullname = os.path.join('SYSTEM','SL.jpg')
    SLImage = pygame.image.load(fullname).convert()
    SLImage = pygame.transform.scale(SLImage,SIZE)
    surface.blit(SLImage,(0,0))

    button_exit = NodeItems.Button(EXIT_POS,EXIT_SIZE,os.path.join('SYSTEM','exit.png'),os.path.join('FONT','hksn.ttf'))
    button_exit.render(surface)
    
    white_buttons_pos = [150,400,650]
    white_buttons = [NodeItems.Button((i,300),(200,200),os.path.join('SYSTEM','white.png'),os.path.join('FONT','hksn.ttf')) for i in white_buttons_pos]
    for i in white_buttons:
        i.render(surface)

    ## get save data
    dict_items , dict_names = savefile_parser()

    if dict_items and dict_names:
        for i in dict_items:
            surface.blit(dict_items[i],(50+250*i,200))

    ##surface.blit(save_image_surface,(50,200))

    ## save behavior
    if g_flag == 'save':
        for (count,i) in enumerate(white_buttons):
            if i.is_over(pos):
                ## Let screenshoting image be displayed
                screen.blit(now_frame,(50+250*count,200))
                ## Save it
                pygame.image.save(now_frame,os.path.join('SAVE',str(count)+'.png'))
                ## Write it to dict
                pickle_elements = (Frame.getNodeIndex(),Frame.getBackground(),Frame.getBGM(),Frame.getPortraits())
                pickled_data = pickle.dumps(pickle_elements) 
                ## storage pickled data
                dict_names[count] = (str(count)+'.png',pickled_data)
                ## Update local datafile
                savefile = open(os.path.join('SAVE','save.dat'),'w')
                ## Write data
                savefile.write(format_save_data(dict_names,savefile))
                savefile.close()
                break
    elif g_flag == 'load':
        for (count,i) in enumerate(white_buttons):
            if i.is_over(pos):
                next_data = dict_names[count][1]
                ## To be sure it is None
                load_data = None
                load_data = next_data
                freeze = False
                break
    ## To exit
    if button_exit.is_over(pos):
        freeze = False


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            ## check where the click point on
            click_point = event.dict['pos']
            surface = nodeItem.getScreen()
            frame = nodeItem
            ## ugly codes...who can tell me
            ## how to write these codes well?
            ## What I wrote were fucking complex
            if dict_settingButtons['save'].is_over(click_point):
                freeze = True
                button_settings(surface,click_point,frame,'save') 
            elif dict_settingButtons['load'].is_over(click_point):
                freeze = True
                button_settings(surface,click_point,frame,'load')
            elif freeze:
                button_settings(surface,click_point,frame)
                ## if load_data is not none
                ## unpickle it and update parser
                ## if load_data:
                ##     pickle_data = pickle.loads(load_data)
                ##     load_data = None
                ##     load_index,load_bg,load_bgm,load_portr = pickle_data
                ##     parser.setNodeIndex(load_index-1)
                ##     parser.setBackground(os.path.basename(load_bg))
                ##     parser.setBGM(os.path.basename(load_bgm))
                ##     parser.setPortrait(load_portr)
                ##     nodeItem.update(parser)
                if load_data:
                    continue


        
                ##if load_index:
                ##    nodeItem.setNextIndex(load_index)
            else:
                if nodeItem.getChoiceButtons():
                    dict_buttons = nodeItem.getChoiceButtons()
                    ##Through over which button been clicked
                    ##Surily if the point out of any button's
                    ##area,we make it freeze :-)

                    for key in dict_buttons.keys():
                        ## each dict_button is a tuple,
                        ## like this (index,button)
                        ## index is the next Node index
                        ## to change the control stream.
                        ## button is a instance of Button
                        index = int(dict_buttons[key][0])
                        button = dict_buttons[key][1]
                        if button.is_over(click_point):
                            nodeItem.setNextIndex(index)
                            break
                
                else:
                    ## pick = pickle.Pickler(f)
                    ## pick.dump((nodeItem.getBGM(),nodeItem.getBackground(),nodeItem.getPortraits()))

                    if load_data:
                        pickle_data = pickle.loads(load_data)
                        load_data = None
                        load_index,load_bg,load_bgm,load_portr = pickle_data
                        parser.setNodeIndex(load_index-1)
                        parser.setBackground(os.path.basename(load_bg))
                        parser.setBGM(os.path.basename(load_bgm))
                        parser.setPortrait(load_portr)
                        nodeItem.update(parser)

                    nodeItem.setNextIndex() 

            
            ##The following codes update screen
            if not freeze:
                NextIndex = nodeItem.getNextIndex() ##get key of one Node
                try:
                    Node = dirNode[NextIndex] ##get a Node which is a string
                    parser.parser(Node)
                    nodeItem.update(parser)
                    
                except KeyError:
                    print 'Cannot search the index:',NextIndex
                    Node = dirNode[ERRORINDEX] ## freeze the inscreasing of index
                    parser.parser(Node)
                    nodeItem.update(parser)
            else:
                pass
        
    clock.tick(8)

    
    pygame.display.update()



