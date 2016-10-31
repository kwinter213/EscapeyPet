import pygame as pg
import math
import random
import time
#import constants --> separate file?

'''' GLOBAL CONSTANTS '''
WIDTH = 369
HEIGHT = 480
FPS = 30 #Framerate

WHITE = (255,255,255)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

TITLE = "ESCAPEY JUMP"

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
		self.image.fill(GREEN)
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

	def new(self):
		#New Game
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
		#AFTTER DRAWING Everything
		pg.display.flip()

	def menu(self):

		pass

	def show_go_screen():

		pass

g = Game()
g.menu()
while g.running:
	g.new()
	g.show_go_screen()

pg.quit()
