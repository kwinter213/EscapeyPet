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
accl = .5
friction = -.13


class Player(pg.sprite.Sprite):

	def __init__(self, game):

		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.image = pg.Surface((30,40))
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect()
		#self.rect.center = (WIDTH /2, HEIGHT/2)
		self.vx = 0
		self.vy = 0

	def update(self):
		self.calc_grav()

		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT]:
			self.vx = -5
		if keys[pg.K_RIGHT]:
			self.vx = 5

		self.rect.x += self.vx
		self.rect.y += self.vy

	def jump(self):
		self.rect.x += 3
		hits = pg.sprite.spritecollide(self, self.game.platforms, False)
		self.rect.x += 3
		if hits:
			self.vel.y = 20

	def calc_grav(self):
		""" Calculate effect of gravity. """
		if self.vy == 0:
			self.vy = 1
		else:
			self.vy += .35

class Platform(pg.sprite.Sprite):
	def __init__(self, x, y, w, h):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((w,h))
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

		p1 = Platform(0, HEIGHT-40, WIDTH, 40)
		self.all_sprites.add(p1)
		self.platforms.add(p1)
		p2 = Platform(WIDTH / 2, HEIGHT * 3/4, 100, 20)
		self.all_sprites.add(p2)
		self.platforms.add(p2)

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
			self.player.rect.y = HEIGHT - hits[0].rect.top
			self.player.vy = 0
			time.sleep(1)
			print self.player.rect.y ## Need a way to stop level

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
