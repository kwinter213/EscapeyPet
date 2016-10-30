''' Escapey Pet Part 2 12pm 10/30
Based off Super Mario Bros platformer game
Some sections adapted from justinmeister, shongsdu,
stackoverflow forums, platform scroller tutorial '''

import pygame, sys, pyganim
from pygame.locals import *
import os
from spritesheet_functions import SpriteSheet #justinmeister

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up the window
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Escapey Pet!')

# set up the colors
'''WHITE = (255, 255, 255)
BLACK = (0, 0, 0) '''
SKYBLUE = (100, 171, 255) #REPLACING WIth BKGD IMAGE
MARIOFONT = pygame.font.Font('mario.ttf', 18) #We could use this but maybe fancier?

# variables (Experiment with them. Still slow)
global platforms
global enemies
x = 100
y = 384
velocityX = 0
velocityY = 0
maxVelocityLeft = -5 #max velocity while walking
maxVelocityRight = 6
maxVelocityLR = -8 #max velocity while running
maxVelocityRR = 9
maxVelocityFall = 6
accX = 0
accY = 0
gravity = 1
onGround = True
collideTop = 0
collideLeft = 0
collideRight = 0
collideBot = 0
moveLeft = False
moveRight = False
running = False
jump = False
flip = False
time = 0
deadTime = 0
levelTime = 0
dead = True
score = 0
coins = 0
levelTimer = 400
startLevel = True
lowTime = False
menu = True
lives = 3
livesScreen = False
livesScreenTime = 0
gameOver = False

#text and menu image -- Make own or find diff font?
hText = MARIOFONT.render('SKEEVY            ESCAPEY PET', True, WHITE)
levelText = MARIOFONT.render('Level 01', True, WHITE)
menuImg = pygame.image.load("menu.jpg") #Need our own menu!
bkground = pygame.image.load("background_2.png")
menuImg = pygame.transform.scale(menuImg, (640, 480))

#Create sprite animations and hitbox
player = pygame.Rect(x, y, 26, 32)

sprite_sheet = SpriteSheet("skeevy2.png") #function from justinmeister
skeevy1 = sprite_sheet.get_image(0, 0, 23, 32)
skeevy2 = sprite_sheet.get_image(84, 0, 26, 27)
skeevy3 = sprite_sheet.get_image(127, 0, 25, 27)
skeevy4 = sprite_sheet.get_image(169, 0, 26, 28)
skeevy5 = sprite_sheet.get_image(126, 43, 27, 26)
skeevy6 = sprite_sheet.get_image(125, 86, 29, 25)
skeevy7 = sprite_sheet.get_image(210, 166, 29, 34)

hWalk = pyganim.PygAnimation([(skeevy1, 0.1), (skeevy2, 0.1),
                                (skeevy3, 0.1), (skeevy4,0.1)])

scoreCoin = pyganim.PygAnimation([('scoreCoin1.png', 0.5), #replace with Cheese
                                  ('scoreCoin2.png', 0.13),
                                  ('scoreCoin3.png', 0.13)])

pyganim.PygAnimation.scale(scoreCoin, (10, 18))
scoreCoin.play()

hWalk1 = sprite_sheet.get_image(126, 43, 27, 26)
hJump = sprite_sheet.get_image(125, 86, 29, 25)
hDead = sprite_sheet.get_image(210, 166, 29, 34)
hJ = pygame.transform.scale(hJump, (28, 32))
hS = pygame.transform.scale(hWalk1, (28, 32))
hD = pygame.transform.scale(hDead, (30, 28))
hF = pygame.transform.flip(hS, 1, 0)
hJL = pygame.transform.flip(hJ, 1, 0)
pyganim.PygAnimation.scale(hWalk, (28, 32))
hWalk.play()


#camera stuff
camera = pygame.Rect(0, 0, 640, 480)

#setup sound -- Different sounds
jumpSound = pygame. mixer.Sound('jump.ogg')
bump = pygame.mixer.Sound('bump.ogg')
coin = pygame.mixer.Sound('coin.ogg')
stomp = pygame.mixer.Sound('stomp.wav')
hDie = pygame.mixer.Sound('mariodie.wav')
speedUp = pygame.mixer.Sound('fastTheme.ogg')
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('pinacolada.mp3') ##MAIN MUSIC THEME - change below too
musicPlaying = True

# tiles  can walk on and hit
#replace platform icons
class Platform():

    def __init__(self, x, y, pic, scaleX, scaleY, fallThrough, animated):
        self.image = pygame.image.load('%s' % (pic))
        if not animated:
            self.floor = pygame.transform.scale(self.image, (scaleX, scaleY))
        else:
            self.aniBlock = pyganim.PygAnimation([('platform-q.png', 0.5),
                                                  ('platform-q2.png', 0.13),
                                                  ('platform-q3.png', 0.13)])
            pyganim.PygAnimation.scale(self.aniBlock, (scaleX, scaleY))
            self.aniBlock.play()
        self.x = x
        self.y = y
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.fallThrough = fallThrough
        self.animated = animated
        self.hit = False

    def update(self, cameraX, cameraY):
        if self.animated and self.hit:
            windowSurface.blit(self.hitImage, (self.x-cameraX, self.y-cameraY))
        elif not self.animated:
            windowSurface.blit(self.floor, (self.x-cameraX, self.y-cameraY))
        else:
            self.aniBlock.blit(windowSurface, (self.x-cameraX, self.y-cameraY))

    def rect(self, cameraX, cameraY):
        return pygame.Rect(self.x-cameraX, self.y-cameraY, self.scaleX, self.scaleY)

    def hitCheck(self, cameraX, cameraY):
        self.hitPic = pygame.image.load("Qhit.png")
        self.hitImage = pygame.transform.scale(self.hitPic, (self.scaleX, self.scaleY))
        if not self.hit:
            coin.play()
        windowSurface.blit(self.hitImage, (self.x-cameraX, self.y-cameraY))
        self.hit = True

#CREATING BIG CHEESE/FINISH LINE


#CREATING POWER UPS
class Powerup(pygame.sprite.Sprite): #adapted from justinarmstrong
    """Base class for all powerup_group"""
    def __init__(self, x, y):
        super(Powerup, self).__init__()

    def setup_powerup(self, x, y, name, setup_frames):
        """This separate setup function allows me to pass a different
        setup_frames method depending on what the powerup is"""
        self.sprite_sheet = setup.GFX['foodicons.png']
        self.frames = []
        self.frame_index = 0
        setup_frames()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.state = c.REVEAL
        self.y_vel = -1
        self.x_vel = 0
        self.direction = c.RIGHT
        self.box_height = y
        self.gravity = 1
        self.max_y_vel = 8
        self.animate_timer = 0
        self.name = name

    def get_image(self, x, y, width, height):
        """Get the image frames from the sprite sheet"""
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)

        image = pg.transform.scale(image,
                                   (int(rect.width*c.SIZE_MULTIPLIER),                                    int(rect.height*c.SIZE_MULTIPLIER)))
        return image

    def update(self, game_info, *args):
        """Updates powerup behavior"""
        self.current_time = game_info[c.CURRENT_TIME]
        self.handle_state()

    def handle_state(self):
        pass

    def revealing(self, *args):
        """Action when powerup leaves the coin box or brick"""
        self.rect.y += self.y_vel

        if self.rect.bottom <= self.box_height:
            self.rect.bottom = self.box_height
            self.y_vel = 0
            self.state = c.SLIDE

    def sliding(self):
        """Action for when powerup slides along the ground"""
        if self.direction == c.RIGHT:
            self.x_vel = 3
        else:
            self.x_vel = -3

    def falling(self):
        """When powerups fall of a ledge"""
        if self.y_vel < self.max_y_vel:
            self.y_vel += self.gravity

class Mushroom(Powerup):
    """Powerup that makes bigger"""
    def __init__(self, x, y, name='mushroom'):
        super(Mushroom, self).__init__(x, y)
        self.setup_powerup(x, y, name, self.setup_frames)


    def setup_frames(self):
        """Sets up frame list"""
        self.frames.append(self.get_image(0, 0, 16, 16))


    def handle_state(self):
        """Handles behavior based on state"""
        if self.state == c.REVEAL:
            self.revealing()
        elif self.state == c.SLIDE:
            self.sliding()
        elif self.state == c.FALL:
            self.falling()

class LifeMushroom(Mushroom):
    """1up mushroom"""
    def __init__(self, x, y, name='1up_mushroom'):
        super(LifeMushroom, self).__init__(x, y)
        self.setup_powerup(x, y, name, self.setup_frames)

    def setup_frames(self):
        self.frames.append(self.get_image(16, 0, 16, 16))

class Enemy():
    def __init__(self, x, y, pic, scaleX, scaleY, deadX, deadY, frames, aniSpeed):
        self.pic = pic
        self.image1 = [('%s%s.png' % (pic, str(num)), aniSpeed) for num in range(frames)]
        self.image = pyganim.PygAnimation(self.image1)
        pyganim.PygAnimation.scale(self.image, (scaleX, scaleY))
        self.image.play()
        self.imageD = pygame.image.load('%sDEAD.png' % (pic))
        self.imageDEAD = pygame.transform.scale(self.imageD, (deadX, deadY))
        self.x = x
        self.y = y
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.dead = False
        self.onGround = True
        self.enemyMove = -1
        self.collide = 0
        self.remove = False
        self.current = False
        self.shellMove = False

    def rect(self, cameraX, cameraY):
        return pygame.Rect(self.x-cameraX, self.y-cameraY, self.scaleX, self.scaleY)

    def update(self, cameraX, cameraY):
        if not self.dead:
            self.image.blit(windowSurface, (self.x-cameraX, self.y-cameraY))
        else:
            windowSurface.blit(self.imageDEAD, (self.x-cameraX, self.y-cameraY+16))

# hardcoded level - next time i'll use a text file
level = """
......................c..........................................................................................................................................................................................................................
...........................................v..................................................v..................................c..............v...............................c................v..............................................
...........c.....................b.............................c...................b.................................c..................b............................c.................b.........................q..c...........................
..........................................................................................1............................................................................................................==........................................
..........................?............................................................++++++++++...++++?................?...........+++....+??+......................................................===........................................
.....................................................................................................................................................................................................====........................................
......................................................................................1.............................................................................................................=====........................................
...................................................................................................................................................................................................======.............w..........................
....................?...+?+?+........................f.........f....................+?+.................+......++.....?..?..?.....+..........++......=..=..........==..=...........++?+...........=======........................................
............................................d.......................................................................................................==..==........===..==........................========........................................
j................................s.....................j..................................................j........................................===..===.j....====..===.....s.............s..=========...j....................................
...............]....h...1...p.................1.[..........11.....]...h.......p...................[......11...........2.]...h.......p..11.11......====p.====....=====..====ph......p....11.....==========...................h....................
---------------------------------------------------------------------------..-----------------....-------------------------------------------------------------------..-------------------------------------------------------------------------------
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~..~~~~~~~~~~~~~~~~~....~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~..~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

def buildLevel(level):
    platX = 0
    platY = 0
    global platforms
    global enemies
    platforms = []
    enemies = []
    for row in level.split("\n"):
        for col in row:
            if col == "-":
                platforms.append( Platform(platX, platY, "floor.png", 32, 32, False, False) )
            if col == "~":
                platforms.append( Platform(platX, platY, "floor.png", 32, 32, True, False) )
            if col == "+":
                platforms.append( Platform(platX, platY, "brick1.png", 32, 32, False, False) )
            if col == "=":
                platforms.append( Platform(platX, platY, "pyramid.png", 32, 32, False, False) )
            if col == "?":
                platforms.append( Platform(platX, platY, "platform-q.png", 32, 32, False, True) )
            if col == "h":
                platforms.append( Platform(platX, platY, "hill.png", 96, 38, True, False) )
            if col == "j":
                platforms.append( Platform(platX, platY, "bighill.png", 160, 70, True, False) )
            if col == "s":
                platforms.append( Platform(platX, platY, "smallpipe.png", 64, 64, False, False) )
            if col == "d":
                platforms.append( Platform(platX, platY, "medpipe.png", 64, 96, False, False) )
            if col == "f":
                platforms.append( Platform(platX, platY, "bigpipe.png", 64, 128, False, False) )
            if col == "c":
                platforms.append( Platform(platX, platY, "smallcloud.png", 64, 48, True, False) )
            if col == "v":
                platforms.append( Platform(platX, platY, "medcloud.png", 96, 48, True, False) )
            if col == "b":
                platforms.append( Platform(platX, platY, "bigcloud.png", 128, 48, True, False) )
            if col == "p":
                platforms.append( Platform(platX, platY, "smallbush.png", 64, 32, True, False) )
            if col == "[":
                platforms.append( Platform(platX, platY, "medbush.png", 96, 32, True, False) )
            if col == "]":
                platforms.append( Platform(platX, platY, "bigbush.png", 128, 32, True, False) )
            if col == "q":
                platforms.append( Platform(platX-16, platY-16, "flag05.png", 48, 336, False, False) )
            if col == "w":
                platforms.append( Platform(platX, platY, "smallcastle.png", 160, 160, True, False) )
            if col == "1":
                enemies.append( Enemy(platX+5, platY, "fly", 32, 32, 32, 16, 2, 0.1) )
            if col == "2":
                enemies.append( Enemy(platX-5, platY-16, "spider", 32, 48, 32, 28, 2, 0.2) )
            platX += 32
        platX = 0
        platY += 32

buildLevel(level)

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

# main game loop
while True:
    BackGround = Background('background_2.png', [0,0])

    # spawn  in level 1
    if livesScreen and pygame.time.get_ticks() - livesScreenTime >= 4000 and not menu:
        if not gameOver:
            livesScreen = False
            camera.x = 0
            camera.y = 0
            player.x = 100
            player.y = 384
            dead = False
            levelTimer = 400
            startLevel = True
            pygame.mixer.music.load('pinacolada.mp3') #MAIN THEME -- above too
            pygame.mixer.music.play(-1, 0.0)
            if flip:
                hWalk.flip(1, 0)
            buildLevel(level)
        else:
            menu = True
            gameOver = False
            lives = 3
            coins = 0
            score = 0

    # check for colliding with platforms
    if not menu:
        windowSurface.fill([255, 255, 255]) #REALLY REALLY SLOW
        windowSurface.blit(BackGround.image, BackGround.rect)

        collideTop = 0
        collideLeft = 0
        collideRight = 0
        collideBot = 0
        for platform in platforms:
            if platform.x - camera.x >= -400 and platform.x - camera.x <= WINDOWWIDTH:
                platform.update(camera.x, camera.y)
                if not platform.fallThrough:
                    if player.colliderect(platform.rect(camera.x, camera.y)) and not dead:
                        if velocityY >= 0 and (player.y < platform.y):
                            player.bottom = platform.rect(camera.x, camera.y).top + 1
                            collideTop += 1
                        elif velocityY < 0 and (player.y >= platform.y + platform.scaleY-5):
                            player.top = platform.rect(camera.x, camera.y).bottom + 2
                            collideBot += 1
                            if platform.animated:
                                if not platform.hit:
                                    coins += 1
                                    score += 200
                                platform.hitCheck(camera.x, camera.y) # ?-blocks turn to already hit animation
                        elif velocityX < 0 and (player.y >= platform.y):
                            player.left = platform.rect(camera.x, camera.y).right + 5
                            collideLeft += 1
                        elif velocityX > 0 and (player.y >= platform.y):
                            player.right = platform.rect(camera.x, camera.y).left - 5
                            collideRight += 1

        # check for colliding with enemies
        for enemy in enemies:
            enemy.collide = 0
            enemy.current = True
            if enemy.dead and pygame.time.get_ticks() - time > 500:
                if not enemy.pic == "fly" or not (enemy.x - camera.x >= -400 and enemy.x - camera.x <= WINDOWWIDTH):
                    enemy.remove = True
            if enemy.x - camera.x >= -400 and enemy.x - camera.x <= WINDOWWIDTH and not enemy.remove:
                enemy.update(camera.x, camera.y)
                if not enemy.onGround and not enemy.dead:
                    enemy.y += 3
                elif not enemy.dead or (enemy.pic == "fly"):
                    enemy.x += enemy.enemyMove
                for platform in platforms:
                    if platform.x - camera.x >= -400 and platform.x - camera.x <= WINDOWWIDTH:
                        if not platform.fallThrough:
                            if enemy.rect(camera.x, camera.y).colliderect(platform.rect(camera.x, camera.y)):
                                if enemy.y < platform.y:
                                    enemy.collide += 1
                                elif enemy.enemyMove < 0:
                                    enemy.enemyMove = 1
                                else:
                                    enemy.enemyMove = -1
                if enemy.collide > 0:
                    enemy.onGround = True
                else:
                    enemy.onGround = False
                for enemy1 in enemies:
                    if enemy1.x - camera.x >= -400 and enemy1.x - camera.x <= WINDOWWIDTH and not enemy1.remove and not enemy1.current:
                        if enemy.rect(camera.x, camera.y).colliderect(enemy1.rect(camera.x, camera.y)):
                                if enemy1.pic == "fly" and enemy1.dead:
                                    enemy.enemyMove = 0
                                    if not enemy.dead:
                                        time = pygame.time.get_ticks()
                                        score += 100
                                    enemy.dead = True
                                if enemy.enemyMove < 0:
                                    enemy.enemyMove = 1
                                else:
                                    enemy.enemyMove = -1
                if player.colliderect(enemy.rect(camera.x, camera.y)) and ( (enemy.pic == "fly") or (not enemy.dead and not dead) ):
                    if player.x < enemy.x and enemy.pic == "fly" and enemy.dead:
                        enemy.enemyMove = 5
                    elif player.x > enemy.x and enemy.pic == "fly" and enemy.dead:
                        enemy.enemyMove = -5
                    elif player.y < enemy.y - 10:
                        enemy.enemyMove = 0
                        stomp.play()
                        velocityY = -9
                        enemy.dead = True
                        time = pygame.time.get_ticks()
                        score += 100
                    if player.y >= enemy.y - 2:
                        if not enemy.dead:
                            dead = True
                            onGround = False
                            moveLeft = False
                            moveRight = False
                            running = False
                            jump = False
                            velocityY = -50
                            velocityX = 0
                            lives -= 1
                            hDie.play()
                            pygame.mixer.music.stop()
                            deadTime = pygame.time.get_ticks()
            enemy.current = False

    #keep track of when is in the air
    if collideTop > 0:
        onGround = True
    else:
        onGround = False
    if collideBot > 0:
        onGround = False
        velocityY = 0
        bump.play()
        jumpSound.stop()
    if collideLeft > 0:
        velocityX = 0
    if collideRight > 0:
        velocityX = 0

    # listen for keystrokes
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_RETURN and menu:
            menu = False
            livesScreen = True
            livesScreenTime = pygame.time.get_ticks()
        if not dead and not menu:
            if event.type == KEYDOWN:
                if event.key == ord('x'):
                    running = True
                if (event.key == K_UP or event.key == K_SPACE or event.key == ord('z')) and onGround:
                    jump = True
                    jumpSound.play()
                    onGround = False
                if event.key == K_LEFT:
                    moveLeft = True
                    moveRight = False
                    flip = True
                    hWalk.flip(1, 0)
                elif event.key == K_RIGHT:
                    moveRight = True
                    moveLeft = False
                    flip = False
            if event.type == KEYUP:
                if (event.key == K_UP or event.key == K_SPACE or event.key == ord('z')):
                    jump = False
                if event.key == ord('x'):
                    running = False
                if event.key == K_LEFT:
                    moveLeft = False
                    hWalk.flip(1, 0)
                elif event.key == K_RIGHT:
                    moveRight = False

    # player movement
    if jump:
        velocityY = -17
        jump = False
    if velocityY < maxVelocityFall:
        velocityY += gravity
    if not onGround or dead:
        player.y += velocityY
    if onGround: #stop velocity when on the ground
        velocityY = 0
    if moveLeft:
        if not running and player.x > 0:
            accX = -.7
            player.x += velocityX
            if velocityX > maxVelocityLeft:
                velocityX += accX
        elif player.x > 0:
            accX = -1.5
            player.x += velocityX
            if velocityX > maxVelocityLR:
                velocityX += accX
    elif moveRight:
        if not running:
            accX = .7
            if player.x < 300:
                player.x += velocityX
            if velocityX < maxVelocityRight:
                velocityX += accX
        else:
            accX = 1.5
            if player.x < 300:
                player.x += velocityX
            if velocityX < maxVelocityRR:
                velocityX += accX

    if velocityX < 0: # friction while running
        velocityX = velocityX + .5
    if velocityX > 0:
        velocityX = velocityX - .5

    if (velocityX < .3 or velocityX > -.3) and not moveLeft and not moveRight:
        velocityX = 0

    if player.x > 299:
        camera.x += velocityX

    # falls off the level, die
    if player.y > 480 and not dead:
        dead = True
        onGround = False
        moveLeft = False
        moveRight = False
        running = False
        jump = False
        velocityX = 0
        lives -= 1
        hDie.play()
        pygame.mixer.music.stop()
        deadTime = pygame.time.get_ticks()

    # Drawing sprites for each direction and action
    if not dead:
        if not onGround:
            if not flip:
                windowSurface.blit(hJ, player)
            else:
                windowSurface.blit(hJL, player)
        elif moveLeft:
            if not jump:
                hWalk.blit(windowSurface, player)
        elif moveRight:
            if not jump:
                hWalk.blit(windowSurface, player)
        elif not moveLeft and not moveRight and onGround:
            if not flip:
                windowSurface.blit(hS, player)
            else:
                windowSurface.blit(hF, player)
    else:
        windowSurface.blit(hD, player)

    # show lives screen between menu and level and after deaths
    if dead and pygame.time.get_ticks() - deadTime > 5000 and not menu and not livesScreen:
        livesScreen = True
        livesScreenTime = pygame.time.get_ticks()

    # play level speed up music when almost out of time
    if levelTimer <= 100 and not lowTime:
        lowTime = True
        pygame.mixer.music.load('#fastTheme.mp3')
        pygame.mixer.music.play(-1, 0.0)
        speedUp.play()

    # if timer reaches 0, die
    if levelTimer == 0 and not dead:
        dead = True
        onGround = False
        moveLeft = False
        moveRight = False
        running = False
        jump = False
        velocityY = -10
        velocityX = 0
        hDie.play()
        pygame.mixer.music.stop()
        deadTime = pygame.time.get_ticks()

    # keep track of level time
    if (pygame.time.get_ticks() - levelTime > 400 or startLevel == True) and levelTimer > 0 and not livesScreen and not menu:
        levelTime = pygame.time.get_ticks()
        levelTimer -= 1
        startLevel = False

    # draw lives screen
    if livesScreen and not menu:
        windowSurface.fill(BLACK)
        if lives > 0:
            livesText = MARIOFONT.render("x  %s" % str(lives), True, WHITE)
            worldText = MARIOFONT.render("WORLD 1-1", True, WHITE)
            windowSurface.blit(livesText, (310, 240))
            windowSurface.blit(worldText, (240, 170))
            windowSurface.blit(hS, (255, 230))
        else:
            if not gameOver:
                gameOverSound.play()
            gameOverText = MARIOFONT.render("GAME OVER", True, WHITE)
            windowSurface.blit(gameOverText, (240, 170))
            gameOver = True

    # draw opening menu screen and scores
    if menu:
        windowSurface.blit(menuImg, (0, 0))
    else:
        scoreText = MARIOFONT.render(str(score).zfill(6), True, WHITE)
        coinText = MARIOFONT.render('x%s' % str(coins).zfill(2), True, WHITE)
        timeText = MARIOFONT.render(str(levelTimer).zfill(3), True, WHITE)
        windowSurface.blit(hText, (50, 15))
        windowSurface.blit(scoreText, (50, 32))
        windowSurface.blit(coinText, (230, 32))
        windowSurface.blit(levelText, (370, 32))
        windowSurface.blit(timeText, (520, 32))
        scoreCoin.blit(windowSurface, (215 ,30))
    pygame.display.update()
    mainClock.tick(60) # Feel free to experiment with any FPS setting.
