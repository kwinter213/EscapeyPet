import pygame
from spritesheetfxn import SpriteSheet

P1_LEFT				= (576, 720, 70, 70)
P1_RIGHT		   	= (576, 576, 70, 70)
P1_MIDDLE		  	= (504, 576, 70, 70)
P2_PLATFORM_LEFT   	= (432, 720, 70, 40)
P2_PLATFORM_MIDDLE 	= (648, 648, 70, 40)
P2_PLATFORM_RIGHT  	= (792, 648, 70, 40)

class Platform(pygame.sprite.Sprite): #what the player jumps
	def __init__(self, spritesheet_im):
		pygame.sprite.Sprite.__init__(self)
		spritesheet = SpriteSheet('tiles_spritesheet.png') #Grabs sheet
		self.image = spritesheet.grabimage(spritesheet_im[0],
										 spritesheet_im[1],
										 spritesheet_im[2],
										 spritesheet_im[3] )
		self.rect = self.image.get_rect() #set reference

class MovingPlatform(Platform): #to do later?
	#Special case platform
	pass
