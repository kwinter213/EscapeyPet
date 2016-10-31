import pygame as pg
import math
import random
import time
import os
#import constants --> separate file?

''' ESCAPEY GAME 2:30pm 10/31

authors: ChristinaHolman, Kim Winter

Help skeevy the hamster reach the top of his cage! Gain points/stay alive

Background:  https://s-media-cache-ak0.pinimg.com/originals/c2/95/4a/c2954a71ecef875d99e3ca224a7d9415.jpg

'''

#UPDATES
''' I added background image, text, etc. Going to change image and add music.
Can you ask the ninjas to help you figure out why the player wont save its y.pos
after it collides with a platform? Once that's checked, try out the jump motion '''

'''' GLOBAL CONSTANTS '''
WIDTH = 369
HEIGHT = 480
FPS = 30 #Framerate
FONT = 'arial'

WHITE = (255,255,255)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

TITLE = "ESCAPEY JUMP" #(VERTICAL SCROLLING)
CURR_DIR = os.path.dirname(os.path.realpath(__file__))

#Starting platforms -- Let's add more variety
PLATFORMLIST = [(0, HEIGHT - 40, WIDTH, 40),
				(WIDTH / 2 - 20, HEIGHT * 3/4, 100, 20),
				(WIDTH/4 - 10, HEIGHT*2, 100, 20),
				(125, HEIGHT -250, 100, 20),
				(150, 100, 75, 20),
				]
class Spritesheet: #THIS pulls images from spritesheet and copies to separate rects
	def __init__(self,filename):
		self.spritesheet = pg.image.load(filename).convert()
	def grabimage(self,x,y,width,height):
		image = pg.Surface([width, height]).convert() #new blank picture
		image.blit(self.spritesheet, (0, 0), (x, y, width, height))
		#This makes a copy of that image and pastes it to a smaller box
		image.set_colorkey(BLACK)
		return image

class Background(pg.sprite.Sprite): #Function used to display background from file
	def __init__(self, image_file, location):
		pg.sprite.Sprite.__init__(self)  #call Sprite initializer
		self.image = pg.image.load(image_file)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

class Player(pg.sprite.Sprite): #Creates the player/user
	vx = 0
	vy = 0
	walkingleft = [] #holds all images of animated walking
	walkingright = []

	def __init__(self, game): #constructs player features and image

		pg.sprite.Sprite.__init__(self)
		self.game = game
		height = 50
		width = 30
		self.image = pg.Surface([width,height])
		self.image.fill(YELLOW)

		#Making the animation frames from spritesheet
		spritesheet = Spritesheet("skeevy2.png")
		skeevy1 = spritesheet.grabimage(0, 0, 23, 32)
		skeevy2 = spritesheet.grabimage(84, 0, 26, 27)
		skeevy3 = spritesheet.grabimage(127, 0, 25, 27)
		skeevy4 = spritesheet.grabimage(169, 0, 26, 28)
		self.walkingright.append(skeevy1)
		self.walkingright.append(skeevy2)
		self.walkingright.append(skeevy3)
		self.walkingright.append(skeevy4)

		image = skeevy2
		skeevy5 = pg.transform.flip(image, True, False)
		self.walkingleft.append(skeevy5)
		image = skeevy3
		skeevy6 = pg.transform.flip(image, True, False)
		self.walkingleft.append(skeevy6)
		image = skeevy4
		skeevy7 = pg.transform.flip(image, True, False)
		self.walkingleft.append(skeevy7)

		self.image = self.walkingright[0]
		self.rect = self.image.get_rect() #set reference
		self.rect.x = (WIDTH/2)
		self.rect.y = (HEIGHT/3)

	def update(self): #update the user thru the game
		self.calc_grav() #Falling motion imitating gravity effect
		
		#sets initial image
		img = (self.rect.x // 30) % len(self.walkingright) 
		self.image = self.walkingright[img]
		
		self.rect.x += self.vx
		
		#if user preses keys:
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT]:
			img = (self.rect.x // 30) % len(self.walkingleft)
			self.image = self.walkingleft[img]			
			self.vx = -5
			
		if keys[pg.K_RIGHT]:
			img = (self.rect.x // 30) % len(self.walkingright)
			self.image = self.walkingright[img]			
			self.vx = 5
		
		#change y position based on velocity	
		self.rect.y += self.vy
		self.vy = 0
		
		#trying to the y-pos at collision to save !
		self.rect.y = self.game.player.rect.y
		print self.rect.y

	def jump(self): #jump movement only when not in air
		self.rect.y += 3
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		self.rect.y += 3
		if hits:
			self.vy = 5

	def calc_grav(self): 
		#The pseudo-gravitational effect

		if self.vy == 0:
			self.vy = 1
		else:
			self.vy += .35


class Platform(pg.sprite.Sprite): #creates our platforms/levers
	def __init__(self, x, y, width, height):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((width, height))
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

background = Background('room.jpg', [0,0]) #makes background image w/ earlier function
class Game: #This is the jumper game
	def __init__(self): #sets up parameters
		pg.init()
		pg.mixer.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		self.running = True
		self.font = pg.font.match_font(FONT)
		
	def new(self): 
		#New Game -- all the things to start with
		self.points = 0
		self.all_sprites = pg.sprite.Group()
		self.player = Player(self)
		self.platforms = pg.sprite.Group()
		self.all_sprites.add(self.player)

		#sets up the platforms
		for platform in PLATFORMLIST:
			p = Platform(*platform)
			self.all_sprites.add(p)
			self.platforms.add(p)

		self.run()

	def run(self):
		# Game Loop -- keeps the game running
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()

	def update(self): #updating thru running mode
		self.all_sprites.update()
		hits = pg.sprite.spritecollide(self.player, self.platforms, False)

		# Check if we are on a platform
		'''This is problematic. Will stop when hits the sides of platform and
		not just top or bottom '''
		if hits:
			self.vy = 0 #stop motion
			#set y-position to player height + platform height
			self.player.rect.y = self.player.rect.height + hits[0].rect.bottom
			
			#debugging: tried resetting pos to 0			
			self.player.rect.y = 0
			
			#debugging: making sure update is actually happening
			print '////////LOL//////////'
			
			#debugging: delay to sit collision			
			time.sleep(2)

		#Scroll further up once reach checkpoint (VERTICAL)
		if self.player.rect.top <= HEIGHT /4:
			self.player.rect.y += abs(self.player.vy) #Move at same vel in opp dir
			for form in self.platforms:
				form.rect.y += abs(self.player.vy)
				if form.rect.top >= HEIGHT:
					form.kill() #get rid of platforms downbelow
					self.points += 10
		#GAME OVER
		if self.player.rect.bottom > HEIGHT:
			#self.playing = False
			for sprite in self.all_sprites:
				sprite.rect.y -= max(self.player.vy, 10)
				if sprite.rect.bottom <0:
					sprite.kill()
		if len(self.platforms) == 0:
			self.playing = False #stop game and restart
		
		#Make new platforms
		while len(self.platforms) < 5:
			width_p = random.randrange(50, WIDTH/2)
			p = Platform(random.randrange(0,WIDTH-width_p),
							random.randrange(-75,-30),
							width_p, 20)
			self.platforms.add(p)
			self.all_sprites.add(p)

	def events(self):
		#GAME LOOP events
		for event in pg.event.get():
			if event.type == pg.QUIT:
				if self.playing:
					self.playing = False
				self.running  = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE:
					self.player.jump()


	def draw(self):
		#things to put on screen
		self.screen.fill(WHITE)
		self.screen.blit(background.image, background.rect)
		self.all_sprites.draw(self.screen)
		self.drawtext(str(self.points),23,WHITE,WIDTH/2,15)
		
		#AFTTER DRAWING Everything
		pg.display.flip()

	def menu(self):

		pass

	def show_go_screen():

		pass

	def drawtext(self, text, size, color, x, y):
		#all the text
		font = pg.font.Font(self.font,size)
		texts = font.render(text,True, color)
		textrect = texts.get_rect()
		textrect.midtop = (x,y)
		self.screen.blit(texts,textrect)

g = Game()
g.menu()
while g.running:
	g.new()
	g.show_go_screen()

pg.quit()
