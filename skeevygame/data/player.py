"""
This module is used to hold the Player class. The Player represents the user-
controlled sprite on the screen.
"""
import pygame

import constants

from platforms import MovingPlatform
from spritesheet_functions import SpriteSheet

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """

    # -- Attributes
    # Set speed vector of player
    change_x = 0
    change_y = 0

    # This holds all the images for the animated walk left/right
    # of our player
    walking_frames_l = []
    walking_frames_r = []

    # What direction is the player facing?
    direction = "R"

    # List of sprites we can bump against
    level = None

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("skeevy2.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(0, 0, 23, 32)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(84, 0, 26, 27)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(127, 0, 25, 27)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(169, 0, 26, 28)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(126, 43, 27, 26)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(125, 86, 29, 25)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(210, 166, 29, 34)
        self.walking_frames_r.append(image)

        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(0, 0, 23, 32)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(84, 0, 26, 27)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(127, 0, 25, 27)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(169, 0, 26, 28)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(126, 43, 27, 26)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(125, 86, 29, 25)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(210, 166, 29, 34)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x
        pos = self.rect.x + self.level.world_shift
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
        self.direction = "L"

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
        self.direction = "R"

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0


'''#Goomba Frames

spritesheet = pygame.image.load("Media/Graphics/smbenemiessheet.png")

character = Surface((16,16),pygame.SRCALPHA)
character.blit(spritesheet,(0,-4))
character = pygame.transform.scale(character, (16*3,16*3))
goombawalk1 = character

character = Surface((16,16),pygame.SRCALPHA)
character.blit(spritesheet,(-30,-4))
character = pygame.transform.scale(character, (16*3,16*3))
goombawalk2 = character

character = Surface((16,16),pygame.SRCALPHA)
character.blit(spritesheet,(-60,0))
character = pygame.transform.scale(character, (16*3,16*3))
goombaflat1 = character

class Goomba(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = -1
        self.yvel = 0
        self.onGround = False
        self.destroyed = False
        self.counter = 0
        self.image = goombawalk1
        self.rect = Rect(x, y, 16*3, 16*3)

    def update(self, platforms, entities):
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100

        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms, entities)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms, entities)

        self.animate()

    def collide(self, xvel, yvel, platforms, entities):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    self.xvel = -abs(xvel)
                    print "collide right"
                if xvel < 0:
                    self.rect.left = p.rect.right
                    self.xvel = abs(xvel)
                    print "collide left"
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
        for p in entities:
            if pygame.sprite.collide_rect(self, p):
                dif = p.rect.bottom - self.rect.top
                if dif <= 8:
                    self.destroyed = True
                    self.counter = 0
                    self.xvel = 0

    def animate(self):
        if not self.destroyed: self.walkloop()
        else: self.destroyloop()

    def walkloop(self):
        if self.counter == 10:
            self.updatecharacter(goombawalk1)
        elif self.counter == 20:
            self.updatecharacter(goombawalk2)
            self.counter = 0
        self.counter = self.counter + 1

    def destroyloop(self):
        if self.counter == 0:
            self.updatecharacter(goombaflat1)
        elif self.counter == 10: self.kill()
        self.counter = self.counter + 1

    def updatecharacter(self, ansurf):
        self.image = ansurf '''
    
