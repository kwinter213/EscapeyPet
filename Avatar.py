#Avatar Code				Kimberly Winter				10/24/16

import sys, pygame
pygame.init()

black= (0,0,0) #initializes the color black
size = width, height = 500,500 #size of the screen
screen = pygame.display.set_mode(size) #initializes the screen size

class Avatar(pygame.sprite.Sprite):
	def __init__(self, image):
		self.image=pygame.image.load(image) #image of skeevy
		self.x=0 #these coordinates don't work, but the ideal starting point is the bottom left corner
		self.y=height 

	def move_left(self): #skeevy moves left
		pass

	def move_right(self): #skeevy moves right
		pass

	def jump(self): #skeevy jumps (following the laws of physics)
		pass

class AvatarViewer(Avatar): #the viewer updates the screen to new coordinates
	def __init__(self, model):
		self.model=model

	def drawAvatar(self, surface): #drawAvatar updates the screen at the "step"
		screen.fill(black)
		screen.blit(self.model.image, [self.model.x, self.model.y])
		pygame.display.flip() 

class Controller(object):
	def __init__(self, models): #models is a list of models
		self.models=models

	def handle_event(self, event):
		if event.type==pygame.KEYUP(): #jump! :D
			pass
		if event.type==pygame.KEYDOWN(): #
			pass


def main():
	controller=Controller()
	while 1: #keeps the screen on 
		for event in pygame.event.get(): #processing list of events that occur
			if event.type == pygame.QUIT: 
				sys.exit()
			controller.handle_event(event)
		Skeevy=Avatar('Skeevy.jpg') #initializes Skeevy
		SkeevyView=AvatarViewer(Skeevy) #initializing the Avatar Viewer
		SkeevyView.drawAvatar(screen) #updates the screen


main()