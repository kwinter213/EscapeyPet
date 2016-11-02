''' ESCAPEY GAME 12:20am 11/3/2016

authors: Christina Holman, Kim Winter

Help skeevy the hamster reach the top of his cage! Gain points & stay alive

Background:  https://s-media-cache-ak0.pinimg.com/originals/c2/95/4a/c2954a71ecef875d99e3ca224a7d9415.jpg
Music: GotG album 'Pina Colada'
Jump sound: 'justinarmstrong' https://github.com/justinmeister/Mario-Level-1/tree/master/resources

'''

import pygame as pg
import math #why did I do this again?
import random
import time
import os
from os import path

'''
***** UPDATES *******
For tomorrow 9am meeting at Olin!
**The resetting y-pos is back (arrgg) but only once reaches 1/4 of bottom ??
**Jump() does work but need to debug for jumping OFF a platforms
**Need to look at stop() being called under events()
**Need to look at calling the jump 'leap' sound
&& Made more comments too.
'''

'''' GLOBAL CONSTANTS '''
WIDTH = 450
HEIGHT = 550
FPS = 30 #Framerate
FONT = 'arial'

WHITE = (255,255,255)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

TITLE = "ESCAPEY JUMP" #(VERTICAL SCROLLING)
self_dir = os.path.dirname(os.path.realpath(__file__))

#Starting platforms -- Let's add more variety
# [x, y, width, height/thickness]
PLATFORMLIST = [(0, HEIGHT - 40, WIDTH, 40), (WIDTH / 2 - 20, HEIGHT * 3/4, 100, 20), #
		(WIDTH/4 - 10, HEIGHT*2, 100, 20), (125, HEIGHT -250, 100, 20),
		(150, 100, 75, 20),
				]

class Spritesheet: #Pulls images from spritesheet and copies to separate rects
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
	height = 50
	width = 30

	def __init__(self, game): #constructs player features and image

		pg.sprite.Sprite.__init__(self)
		self.game = game #calls all the Game elements for access here
		self.rightSide = WIDTH - self.width #determines the Right limit of player
		self.image = pg.Surface([self.width,self.height]) #makes rect space for image
		self.image.fill(YELLOW)

		#Making the animation frames from spritesheet
		spritesheet = Spritesheet("skeevy2.png") #uses spritesheet with fxn above
		skeevy1 = spritesheet.grabimage(0, 0, 23, 32) #images for walking frames
		skeevy2 = spritesheet.grabimage(84, 0, 26, 27)
		skeevy3 = spritesheet.grabimage(127, 0, 25, 27)
		skeevy4 = spritesheet.grabimage(169, 0, 26, 28)
		self.walkingright.append(skeevy1) #images for walking RIGHT
		self.walkingright.append(skeevy2)
		self.walkingright.append(skeevy3)
		self.walkingright.append(skeevy4)
		self.screenrect = pg.Rect((0,0), (WIDTH, HEIGHT)) #grabs rect of entire screen

		image = skeevy2 #images for walking LEFT (reveresed RIGHT ones)
		skeevy5 = pg.transform.flip(image, True, False)
		self.walkingleft.append(skeevy5)
		image = skeevy3
		skeevy6 = pg.transform.flip(image, True, False)
		self.walkingleft.append(skeevy6)
		image = skeevy4
		skeevy7 = pg.transform.flip(image, True, False)
		self.walkingleft.append(skeevy7)

		self.image = self.walkingright[0] #sets image to walking animation
		self.rect = self.image.get_rect() #set reference rectangle
		self.rect.x = (WIDTH/2) #centers avatar
		self.rect.y = (HEIGHT/3)

	def update(self): #update the user thru the game
		self.calc_grav() #Falling motion imitating gravity effect

		#sets initial image
		img = (self.rect.x // 30) % len(self.walkingright)
		self.image = self.walkingright[img]
		if self.rect.x >= 0 or self.rect.x <= WIDTH: #make sure we are in the frame
			self.rect.x += self.vx

		#if user preses keys:
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT]:
			img = (self.rect.x // 30) % len(self.walkingleft) #change image --> animation
			self.image = self.walkingleft[img]
			self.vx = -5 #move 5 in Left direction

		if keys[pg.K_RIGHT]:
			img = (self.rect.x // 30) % len(self.walkingright)
			self.image = self.walkingright[img]
			self.vx = 5 #move 5 in Right direction

		#change y position based on velocity
		self.rect.y += self.vy
		self.vy = 0 #stop afterwards
		'''DEBUG: vx = 0 '''

		#trying to the y-pos at collision height (save last y value)
		self.rect.y = self.game.player.rect.y
		if (self.rect.x > self.rightSide): #don't go past right edge
			self.rect.x = self.rightSide
		if self.rect.x < self.width: #don't go past leftside of screen
			self.rect.x = self.width


	def jump(self): #jump movement only when not in air
		#check if we hit anything
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		''' NEED TO SWITCH IF-ELSE. WANT TO JUMP ONLY IF ON SOLID '''
		if hits: #dont move if we hit something
			self.dy = 0
		else: #if we arent, move
			self.rect.y -= 5
			#self.rect.y -= 3 #since have falling effect, dont need this?

		''' FIXED _DEBUG: jump
		print '+++++++JUMP+++++++'
		print self.rect.y '''

	def stop(self):
		'''DEBUG: Not being called correctly in events()'''
		#if we hit anything don't move
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		if hits == False: #actually not sure if we need the if statement
			self.vx = 0
			self.vy = 0

	def calc_grav(self):
		#The pseudo-gravitational effect
		if self.vy == 0: #if not moving, big pull
			self.vy = 1
		else: #increase slightly after/incrementally
			self.vy += .35

class Platform(pg.sprite.Sprite): #creates our platforms/levers
	def __init__(self, x, y, width, height):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((width, height))
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect() #i dont think we need a sprite
		self.rect.x = x
		self.rect.y = y

background = Background('room.jpg', [0,0]) #makes background image w/ earlier function
class Game: #This is the jumper game
	def __init__(self): #sets up parameters
		pg.init()
		pg.mixer.init() #open music fxn
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock() #set the internal clock
		self.running = True
		self.font = pg.font.match_font(FONT) #create font
		self.dir = path.dirname(__file__) #look in current folder

	def load(self):
		self.dir = path.dirname(__File__) #look for file in current folder
		#could make a sound for each jump
		self.leap = pg.mixer.Sound(path.join(self.dir, 'leap.ogg'))

	def new(self):
		#New Game -- all the things to start with
		self.points = 0 #resets score
		self.all_sprites = pg.sprite.Group()
		self.player = Player(self) #link to fxn
		self.platforms = pg.sprite.Group() #create group for platforms
		self.all_sprites.add(self.player) #create set for all pieces

		#sets up the platforms
		for platform in PLATFORMLIST: #look in global list
			p = Platform(*platform) #set up each platform in list
			self.all_sprites.add(p) #add them all to sprite group
			self.platforms.add(p) #add them to the platforms set
		#MAIN THEME. I'll put MarvinGaye in there too
		pg.mixer.music.load(path.join(self.dir, 'pinacolada.mp3'))
		self.run()

	def run(self):
		# Game Loop -- keeps the game running
		pg.mixer.music.play(-1) #keep infinite theme song
		self.playing = True #tells to play
		while self.playing: #all the fxns to draw from
			self.clock.tick(FPS) #start clock
			self.events() #play scene by scene
			self.update() #update the scene
			self.draw() #display the scene
		pg.mixer.music.fadeout(300) #fades music out nicely

	def update(self): #updating while running
		self.all_sprites.update() #update each sprite

		# Check if we are on a platform
		'''oK IT IS STOPPING. BUT MAYBE TOO HIGH above platform? '''
		hits = pg.sprite.spritecollide(self.player, self.platforms, False)
		if hits:
			#set y-position to where platform is
			'''DEBUG: resets at center height once hits 1/4 from bottom '''
			self.player.rect.y = hits[0].rect.bottom - 20
			self.vy = 0 #stop motion

			'''DEBUG: Stop at xy of platform '''

		#Scroll further up once reach checkpoint (VERTICAL)
		if self.player.rect.top <= HEIGHT/4: #when reach 3/4 of screen height
			#Move at vel of player in opp direction
			self.player.rect.y += abs(self.player.vy)
			for form in self.platforms: #for each platform in set
				form.rect.y += abs(self.player.vy) #decrease height by player vel
				if form.rect.top >= HEIGHT: #when it goes off screen
					form.kill() #get rid of platforms downbelow
					self.points += 10 #increase our point total
		#GAME OVER
		if self.player.rect.bottom > HEIGHT: #player falls off
			self.playing = False #stop game
			for sprite in self.all_sprites: #make it seem we're falling
				sprite.rect.y -= max(self.player.vy, 10)
				''' Check if this in in right direction (up) '''
				if sprite.rect.bottom <0: #goes off screen, delete it
					sprite.kill()
		if len(self.platforms) == 0: #if we delete all platforms
			self.playing = False #stop game and restart
			print '+++++++++ RESTART ++++++++++'

		#Make new platforms
		while len(self.platforms) < 5: #num of platforms in set
			width_p = random.randrange(50, WIDTH/2) #randomize width
			#make platform with random height, width, location
			#keep thickness at 20 though
			p = Platform(random.randrange(0,WIDTH-width_p),
							random.randrange(-75,-30),
							width_p, 20)
			self.platforms.add(p) #add new platforms to set
			self.all_sprites.add(p) #and to all sprites

	def events(self): #if user does something // input
		#GAME LOOP events
		for event in pg.event.get():
			if event.type == pg.QUIT: #if closes game
				if self.playing:
					self.playing = False #turn play mode OFF
				self.running  = False #stop running code
			if event.type == pg.KEYDOWN: #if hits key
				if event.key == pg.K_SPACE: #and it's spacebar
					self.player.jump() #make avatar jump
					'''DEBUG: calling it properly'''
					#self.load.leap.play() #make jumping noise
			if event.type == pg.KEYUP: #if no hands on keyboard
				self.player.stop() #stop the avatar from moving

	def draw(self):
		#things to put on screen
		self.screen.fill(WHITE) #make white screen
		#set background with Background fxn (class)
		self.screen.blit(background.image, background.rect)
		#draw all the sprites made
		self.all_sprites.draw(self.screen)
		#put text at top with points calculated
		self.drawtext('SKEEVY ESCAPES                  SCORE: '+str(+self.points),23,WHITE,WIDTH/2,15)


		#AFTTER DRAWING Everything
		pg.display.flip() #make it visible

	def menu(self):
		#wanted to make a main menu or welcome screen
		#like pause or last/high-score
		pass

	def show_go_screen():
		#make a start screen
		pass

	def drawtext(self, text, size, color, x, y):
		#all the text I want to show
		font = pg.font.Font(self.font,size) #set the font
		texts = font.render(text,True, color) #set the text
		textrect = texts.get_rect() #set in rectangle space
		textrect.midtop = (x,y) #position at midpoint
		self.screen.blit(texts,textrect) #put text on the space

g = Game() #notation for Game definiton
g.menu() #show the menu if not playing
while g.running: #if running game
	g.new() #set up game environment
	g.show_go_screen() #show welcome/start screen

pg.quit() #stop code
