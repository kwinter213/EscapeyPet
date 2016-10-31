#Avatar Code				Kimberly Winter				10/24/16

import sys, pygame
pygame.init()

black= (0,0,0) #initializes the color black
size = width, height = 500,500 #size of the screen
screen = pygame.display.set_mode(size) #initializes the screen size
floor= 0 #x-coordinate of the floor

class Avatar(pygame.sprite.Sprite):
	def __init__(self, image):
		self.image=pygame.image.load(image) #image of skeevy
		self.x=0 #these coordinates don't work, but the ideal starting point is the bottom left corner
		self.y=floor
		self.dx=0
		self.dy=0

	def step(self): #steps skeevy using acceleration
		self.x=self.x+self.dx
		self.y=self.y=self.dy
		SkeevyView.drawAvatar(screen)

	def move_left(self): #skeevy moves left
		self.dx=-5
		self.step()
		self.dx=0

	def move_right(self): #skeevy moves right
		self.dx=5
		self.step()
		self.dx=0

	def jump(self): #skeevy jumps (following the laws of physics (but changing the gravitational constant to make it easier to jump)))
		self.dy=10
		while(self.x>=floor): #when we figure out how collisions work, we need to implement that too
			self.dy=-1
			self.step()
		self.dy=0


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
		if event.type==pygame.MOUSEBUTTONDOWN: #jump! :D
			self.models[0].move_right() #specific to Skeevy being the first model
		if event.type==pygame.KEYDOWN: #need to figure out how these pygame commands work
			pass

Skeevy=Avatar('skeevy.jpg') #initializes Skeevy
SkeevyView=AvatarViewer(Skeevy) #initializing the Avatar Viewer
models= [Skeevy]
controller=Controller(models)

def main():
	while 1: #keeps the screen on 
		for event in pygame.event.get(): #processing list of events that occur
			if event.type == pygame.QUIT: 
				sys.exit()
			controller.handle_event(event)
		SkeevyView.drawAvatar(screen) #updates the screen


main()
