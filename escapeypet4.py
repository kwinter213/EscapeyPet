''' Escapey Pet Part 3 3:30pm 10/30

Consulted code: justinmeister, shongsdu, stackoverflow forums,
platform scroller tutorial

Spritesheet art = http://tsgk.captainn.net/index.php?p=search&q=Hamtaro
Free Font = http://www.webpagepublicity.com/free-fonts-x.html
'''

import pygame, sys
import time
import os
import constants as c

P1_LEFT			= (576, 720, 70, 70)
P1_RIGHT		   = (576, 576, 70, 70)
P1_MIDDLE		  = (504, 576, 70, 70)
P2_PLATFORM_LEFT   = (432, 720, 70, 40)
P2_PLATFORM_MIDDLE = (648, 648, 70, 40)
P2_PLATFORM_RIGHT  = (792, 648, 70, 40)

#SPRITESHEET function -- from spritesheet tutorial arcadegames
class SpriteSheet(object): #to grab single images from a sheet of images
	spritesheet = None
	def __init__(self, filename): #
		self.spritesheet = pygame.image.load(filename).convert()
		#Will load the sheet of images
	def grabimage(self, x, y, width, height):
		"""Given the x-y location of the image we want, grab pic of said width
		and height """
		image = pygame.Surface([width, height]).convert() #new blank picture
		image.blit(self.spritesheet, (0, 0), (x, y, width, height))
		#This makes a copy of that image and pastes it to a smaller box
		image.set_colorkey(c.BLACK)
		return image


class Platform(pygame.sprite.Sprite): #what the player jumps
	def __init__(self, spritesheet_im):
		pygame.sprite.Sprite.__init__(self)
		spritesheet = SpriteSheet('platforms.png') #Grabs sheet
		self.image = spritesheet.grabimage(spritesheet_im[0],
										 spritesheet_im[1],
										 spritesheet_im[2],
										 spritesheet_im[3] )
		self.rect = self.image.get_rect() #set reference

class MovingPlatform(Platform): #to do later?
	#Special case platform
	pass

class Level(): #used to define all the levels '''
	platforms = None
	enemies = None
	background = None

	#Amount we're scrolling -- tutorial
	worldturns = 0
	lvlimit = -1000
	def __init__(self, avatar):
			#Make list of all sprites in all levels
			self.platforms = pygame.sprite.Group()
			self.enemies = pygame.sprite.Group()
			self.avatar = avatar

	#Update everything
	def update(self):
		''' Update everything in Level x '''
		self.platforms.update()
		self.enemies.update()
	def draw(self, window):
		#Draw the background
		window.fill(c.BLUE)
		window.blit(self.background, (self.worldturns // 3, 0))
		self.platforms.draw(window)
		self.enemies.draw(window)
	def turnworld(self, shiftx):
		''' When avatar moves, scroll all components '''
		self.worldturns += shiftx
		for platform in self.platforms:
			platform.rect.x += shiftx
		for enemy in self.enemies:
			enemy.rect.x += shiftx

class Level01(Level):
	''' Going to setup level 1 '''
	def __init__(self, avatar):
		Level.__init__(self, avatar)
		self.background = pygame.image.load("background_1.png")
		self.background.set_colorkey(c.WHITE)
		self.lvlimit = -2500 #??

		#Array with platform types and locations -- ADD MORE
		level = [   [P1_LEFT, 500, 500],
					[P1_MIDDLE, 580, 490],
					[P1_RIGHT, 620, 500],
					[P1_MIDDLE, 720, 300],
				]
		for platform in level: #Go through array and add
			block = Platform(platform[0])
			block.rect.x = platform[1]
			block.rect.y = platform[2]
			block.avatar = self.avatar
			self.platforms.add(block)

		'''block = MovingPlatforms(Platform.P1_MIDDLE)
		block.rect.x = 1300
		block.rect.y = 250
		block.edge_left = 1300
		block.edge_right = 1500
		block.dx = 1
		block.avatar = self.avatar
		block.level = self
		self.platforms.add(block)'''

class Level02(Level):
	def __init__(self, avatar):
		Level.__init__(self, avatar)
		self.background = pygame.image.load("background_2.png")
		self.background.set_colorkey(c.WHITE)
		self.lvlimit = -2500 #??

		#Array with platform types and locations -- ADD MORE
		level = [   [P1_LEFT, 500, 500],
					[P1_MIDDLE, 580, 490],
					[P1_RIGHT, 620, 500],
					[P1_MIDDLE, 720, 300],
				]
		for platform in level: #Go through array and add
			block = Platform(platform[0])
			block.rect.x = platform[1]
			block.rect.y = platform[2]
			block.avatar = self.avatar
			self.platforms.add(block)

class Avatar(pygame.sprite.Sprite):
	level = None #sprites avatar can collide with
	dx = 0
	dy = 0
	walkingleft = [] #holds all images of animated walking, flipped
	walkingright = []
	facing = 'R'

	def __init__(self): #Kim: removed *image to make animation
		pygame.sprite.Sprite.__init__(self)

		spritesheet = SpriteSheet('skeevy2.png')
		#Images just for walking right
		skeevy1 = spritesheet.grabimage(0, 0, 23, 32)
		skeevy2 = spritesheet.grabimage(84, 0, 26, 27)
		skeevy3 = spritesheet.grabimage(127, 0, 25, 27)
		skeevy4 = spritesheet.grabimage(169, 0, 26, 28)
		self.walkingright.append(skeevy1)
		self.walkingright.append(skeevy2)
		self.walkingright.append(skeevy3)
		self.walkingright.append(skeevy4)

		#Images just for walking left
		image = skeevy2
		skeevy5 = pygame.transform.flip(image, True, False)
		self.walkingleft.append(skeevy5)

		image = skeevy3
		skeevy6 = pygame.transform.flip(image, True, False)
		self.walkingleft.append(skeevy6)

		image = skeevy4
		skeevy7 = pygame.transform.flip(image, True, False)
		self.walkingleft.append(skeevy7)

		#But start with frame 0
		self.image = self.walkingright[0]
		self.rect = self.image.get_rect() #set reference


	def update(self): #Moves avatar'
		self.rect.x += self.dx #Subset of the full rectangle
		#self.gravity()??

		position = self.rect.x + self.level.worldturns #level.
		if self.facing == "R":
			img = (position // 30) % len(self.walkingright)
			self.image = self.walkingright[img]
		else:
			frame = (position // 30) % len(self.walkingleft)
			self.image = self.walkingleft[img]

		#Did we hit anything?
		collisions = pygame.sprite.spritecollide(self, self.level.platforms, False)
		for collision in collisions:
			#Reset position
			if self.dx > 0:
				self.rect.right =  collision.rect.left
			elif self.dx < 0:
				self.rect.left = collision.rect.right
			#Stop movement in y-direction
			self.dy = 0
			''' add for Moving Platform ???'''

		#Then move and do same check for y
		self.rect.y += self.dx
		collisions = pygame.sprite.spritecollide(self, self.Level.platforms, False)
		for collision in collisions:
			#Reset position
			if self.dy > 0:
				self.rect.ground =  collision.rect.top
			elif self.dy < 0:
				self.rect.top = collision.rect.ground

		#Stop movement in y-direction
		self.dy = 0

	def jump(self):
		self.rect.y += 3 #Need to move the whole rectangle/image
		collisions = pygame.sprite.spritecollide(self, self.Level.platforms, False)
		self.rect.y -= 3
		if len(collisions) > 0 or self.rect.ground >= c.SCREEN_HEIGHT:
			self.dy= -10
			#Need a better way to check if we can jump?
		while(self.x >= groundlevel):
			self.y+=self.dy
			self.dy+=-1

	def move_left(self): #skeevy moves left
		self.dx = -5
		self.x = self.x + self.dx
		self.facing = "L"

	def move_right(self): #skeevy moves right
		self.dx=5
		self.x=self.x+self.dx #Not sure if this is necessary?
		self.facing = "R"

	def gravity(self):
		#I feel like we should have an actual gravity eqn
		pass

	def stop(self): #''' when no hands on keyboard '''
		self.dx = 0

def main(): # MAIN PROGRAM
	pygame.init()
	size = [c.SCREEN_WIDTH, c. SCREEN_HEIGHT]
	window = pygame.display.set_mode(size)
	pygame.display.set_caption("Escapey Pet!!")

	avatar = Avatar() #create avatar
	leveln = [] #list of all levels
	leveln.append(Level01(avatar))
	leveln.append(Level02(avatar))

	#set current level
	currentleveln = 0
	currentlevel = leveln[currentleveln]
	sprites_active = pygame.sprite.Group()
	avatar.rect.x = 340
	avatar.rect.y = c.SCREEN_HEIGHT - avatar.rect.top
	sprites_active.add(avatar)

	#Loop until close button -->> Game over
	done = False
	clock = pygame.time.Clock()

	''' ====== MAIN LOOP ======= '''
	while not done:
		for event in pygame.event.get(): #user Action
			if event.type == pygame.QUIT: #if close button
				done = True #straightforward
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					avatar.move_left()
				if event.key == pygame.K_RIGHT:
					avatar.move_right()
				if event.key == pygame.K_UP:
					avatar.jump()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT and avatar.dx <0:
					avatar.stop()
				if event.key == pygame.K_RIGHT and avatar.dx >0:
					avatar.stop()

		sprites_active.update()
		currentlevel.update()

		#Shifting the world as we scroll
		if avatar.rect.right >= 500:
			diff = avatar.rect.right - 500
			avatar.rect.right = 500
			currentlevel.turnworld(-diff)
		if avatar.rect.left <= 120:
			diff = 120 - avatar.rect.left
			avatar.rect.left = 120
			currentlevel.turnworld(diff)

		#If player gets to end of the level...
		currentpos = avatar.rect.x + currentlevel.worldturns
		if currentpos < currentlevel.lvlimit:
			avatar.rect.x = 120
			if currentlevel < len(levels)-1:
				currentlevel += 1
				currentlevel = levels[currentlevel]
				avatar.level = currentlevel

		#Draw
		currentlevel.draw(window)
		sprites_active.draw(window)

		clock.tick(60) #limits to 60 frames per sections
		pygame.display.flip()

	pygame.quit()

if __name__ == '__main__':
	main()
