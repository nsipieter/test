
import pygame               
from pygame.locals import * 
from sys import exit        
 
screen_size = (800,600)     
 
class IsoGame(object):
  def __init__(self):
    pygame.init()       
    flag = DOUBLEBUF    
    self.surface = pygame.display.set_mode(screen_size,flag)
    self.gamestate = 1  # 1 - run, 0 - exit
    self.pic = pygame.image.load('tree.png') # Upload an image to a memory
    self.x= 500
    self.y= 20
    self.speed = 1.2
    # initial screen drawing
    self.surface.blit(self.pic, (self.x, self.y)) 
    pygame.display.flip()
    self.loop()

  def game_exit(self):
    """ quit """
    exit()

  def loop(self):
    """ main loop """
    while self.gamestate==1:
      for event in pygame.event.get():
        if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
          self.gamestate=0
      keys = pygame.key.get_pressed()
      self.events(keys) 
    self.game_exit()

  def events(self, keys):
    """ events processing """
    if keys[K_q]:      
      self.x -= (5*self.speed)
    if keys[K_d]:      
      self.x += (5*self.speed)
    if keys[K_z]:      
      self.y -= (5*self.speed)
    if keys[K_s]:      
      self.y += (5*self.speed)

    #collision()
    self.surface.fill((0,0,0)) 
    self.surface.blit(self.pic, (self.x, self.y))  
    pygame.display.flip()

def collision(self, rect1, rect2):
  pass

if __name__ == '__main__':
   IsoGame()