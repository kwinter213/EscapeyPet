import pygame as pg
import math
import random
import time
#import constants --> separate file?

''' ESCAPEY GAME 2:30pm 10/31

authors: Christin aHolman, Kim Winter

Help skeevy the hamster reach the top of his cage! Gain points/stay alive

'''

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

#Starting platforms -- Let's add more variety
PLATFORMLIST = [(0, HEIGHT - 40, WIDTH, 40),
				(WIDTH / 2 - 20, HEIGHT * 3/4, 100, 20),
				(WIDTH/4 - 10, HEIGHT*2, 100, 20),
				(125, HEIGHT -250, 100, 20),
				(150, 100, 75, 20),
				]

class Player(pg.sprite.Sprite):
	vx = 0
	vy = 0
	print 'STILL HERE'
	def __init__(self, game):

		pg.sprite.Sprite.__init__(self)
		self.game = game
		height = 50
		width = 30
		self.image = pg.Surface([width,height])
		self.image.fill(YELLOW)

		self.rect = self.image.get_rect()
		self.rect.x = (WIDTH/2)
		self.rect.y = (HEIGHT/3)

	def update(self):
		self.calc_grav()

		self.rect.x += self.vx
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT]:
			self.vx = -5
		if keys[pg.K_RIGHT]:
			self.vx = 5
		self.rect.y += self.vy
		self.vy = 0
		self.rect.y = self.game.player.rect.y
		print self.rect.y

	def jump(self):
		self.rect.y += 3
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		self.rect.y += 3
		if hits:
			self.vy = 5

	def calc_grav(self):
		""" Calculate effect of gravity. """

		if self.vy == 0:
			self.vy = 1
		else:
			self.vy += .35

		'''if self.rect.y >= HEIGHT - self.rect.height and self.vy >= 0:
			self.rect.y = 2
			self.vy = 0
		print 'AFTER'
		print self.rect.y '''

class Platform(pg.sprite.Sprite):
	def __init__(self, x, y, width, height):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((width, height))
		self.image.fill(PURPLE)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Game:
	def __init__(self):
		pg.init()
		pg.mixer.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		self.running = True
		self.font = pg.font.match_font(FONT)

	def new(self):
		#New Game
		self.points = 0
		self.all_sprites = pg.sprite.Group()
		self.player = Player(self)
		self.platforms = pg.sprite.Group()
		self.all_sprites.add(self.player)

		for platform in PLATFORMLIST:
			p = Platform(*platform)
			self.all_sprites.add(p)
			self.platforms.add(p)

		self.run()

	def run(self):
		# Game Loop
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()

	def update(self):
		self.all_sprites.update()
		hits = pg.sprite.spritecollide(self.player, self.platforms, False)

		# See if we are on platform
		if hits:
			self.vy = 0
			self.player.rect.y = self.player.rect.height + hits[0].rect.bottom
			self.player.rect.y = 0
			print '////////LOL//////////'
			time.sleep(2)

		#Scroll further up once reach checkpoint (VERTICAL)
		if self.player.rect.top <= HEIGHT /4:
			self.player.rect.y += abs(self.player.vy) #Move at same vel in opp direction
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
		#Draw / render
		self.screen.fill(WHITE)
		self.all_sprites.draw(self.screen)
		self.drawtext(str(self.points),23,WHITE,WIDTH/2,15)
		#AFTTER DRAWING Everything
		pg.display.flip()

	def menu(self):

		pass

	def show_go_screen():
		pass

	def drawtext(self, text, size, color, x, y):
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
