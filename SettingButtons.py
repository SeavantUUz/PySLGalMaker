# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from sys import exit
import os

SIZE = (800,600)

def save(surface,pos):
    fullname = os.path.join('SYSTEM','SL.jpg')
    SLImage = pygame.image.load(fullname).convert()
    SLImage = pygame.transform.scale(SLImage,SIZE)
    surface.blit(SLImage,(0,0))
     
