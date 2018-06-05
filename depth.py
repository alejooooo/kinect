#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 20 18:40:04 2018

@author: alejandro
"""
import sys  
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
import pygame
import numpy as np
import sys
from freenect import sync_get_depth as get_depth

	
#funcion asigna la superficie de colores
def make_gamma():

    num_pix = 2048 # valores posibles de profundidad NO JUGAR
    npf = float(num_pix)
    _gamma = np.empty((num_pix, 3), dtype=np.uint16)
    for i in xrange(num_pix):
        v = i / npf
        v = pow(v, 3) * 6
        pval = int(v * 35  * 256-500) # cambiar profundidad  -----------40-------------- 
        lb = pval & 0xf1
        pval >>= 8
        if pval == 0:
            a = np.array([255, 255 - lb, 255 - lb], dtype=np.uint8)
        elif pval == 1:
            a = np.array([255, lb, 0], dtype=np.uint8)
        elif pval == 2:
            a = np.array([255 - lb, lb, 0], dtype=np.uint8)
        elif pval == 3:
            a = np.array([255 - lb, 255, 0], dtype=np.uint8)
        elif pval == 4:
            a = np.array([0, 255 - lb, 255], dtype=np.uint8)
        elif pval == 5:
            a = np.array([0, 0, 255 - lb], dtype=np.uint8)
        else:
            a = np.array([0, 0, 0], dtype=np.uint8)

        _gamma[i] = a
    return _gamma


gamma = make_gamma()


if __name__ == "__main__":
    fpsClock = pygame.time.Clock()
    FPS = 30 # FPS
    disp_size = (1280, 760)
    resolucion = (640, 480)
    pygame.init()
    screen = pygame.display.set_mode(disp_size)
    font = pygame.font.Font('e14.otf', 32) # OJO CON LA FUENTE
    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                sys.exit()
        fps_text = "FPS: {0:.2f}".format(fpsClock.get_fps())


        depth = np.rot90(get_depth()[0]) # lectura de profundidad
        pixels = gamma[depth] # color dado por gamma
        temp_surface = pygame.Surface(resolucion)
        pygame.surfarray.blit_array(temp_surface, pixels)
        pygame.transform.scale(temp_surface, disp_size, screen)
        screen.blit(font.render(fps_text, 1, (255, 255, 255)), (15, 15))
        pygame.display.flip()
        fpsClock.tick(FPS)
