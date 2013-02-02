# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from sys import exit
from sys import getsizeof
import NodeItems
import Parser

ERRORINDEX = 65535

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

nodeItem = NodeItems.NodeItem(screen)
parser.parser(dirNode[0])
nodeItem.update(parser)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            ## check where the click point on
            if nodeItem.getChoiceButtons():
                click_point = event.dict['pos']
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
                nodeItem.setNextIndex()

            
            ##The following codes update screen
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
        
    clock.tick(5)

    
    pygame.display.update()



