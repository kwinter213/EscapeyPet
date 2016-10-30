import pygame

import constants
import platforms
'''import collider
import enemies
import checkpoint
import score'''

class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    # Lists of sprites used in all levels. Add or remove
    # lists as needed for your game. """
    platform_list = None
    enemy_list = None

    # Background image
    background = None

    # How far this world has been scrolled left/right
    world_shift = 0
    level_limit = -1000

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
	'''self.setup_enemies()
	self.setup_checkpoints()'''

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        # We don't shift the background as much as the sprites are shifted
        # to give a feeling of depth.
        screen.fill(constants.BLUE)
        screen.blit(self.background,(self.world_shift // 3,0))

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

	'''def setup_ground(self):
        #Collideable, invisible rectangles over top for sprites to walk on
            ground_rect1 = collider.Collider(0, c. GROUND_HEIGHT, 2953, 60)
            ground_rect2 = collider.Collider(3048, c.GROUND_HEIGHT, 635, 60)
            ground_rect3 = collider.Collider(3819, c.GROUND_HEIGHT, 2735, 60)
            ground_rect4 = collider.Collider(6647, c.GROUND_HEIGHT, 2300, 60)

        self.ground_group = pg.sprite.Group(ground_rect1, ground_rect2, ground_rect3, ground_rect4)


	def setup_checkpoints(self):
        #Creates invisible checkpoints that when collided will trigger
        #the creation of enemies from the self.enemy_group_list"""
            check1 = checkpoint.Checkpoint(510, "1")
            check2 = checkpoint.Checkpoint(1400, '2')
            check3 = checkpoint.Checkpoint(1740, '3')
            check4 = checkpoint.Checkpoint(3080, '4')
            check5 = checkpoint.Checkpoint(3750, '5')
            check6 = checkpoint.Checkpoint(4150, '6')
            check7 = checkpoint.Checkpoint(4470, '7')
            check8 = checkpoint.Checkpoint(4950, '8')
            check9 = checkpoint.Checkpoint(5100, '9')
            check10 = checkpoint.Checkpoint(6800, '10')
            check11 = checkpoint.Checkpoint(8504, '11', 5, 6)
            check12 = checkpoint.Checkpoint(8775, '12')
            check13 = checkpoint.Checkpoint(2740, 'secret_mushroom', 360, 40, 12)

	    self.check_point_group = pg.sprite.Group(check1, check2, check3,
		                                         check4, check5, check6,
		                                         check7, check8, check9,
		                                         check10, check11, check12,
		                                         check13)
	def setup_spritegroups(self):
        #Sprite groups created for convenience"""
	    self.sprites_about_to_die_group = pg.sprite.Group()
	    self.shell_group = pg.sprite.Group()
	    self.enemy_group = pg.sprite.Group() '''


# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("background_1.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -2500

        # Array with type of platform, and x, y location of the platform.
	## SHOULD REPLACE WITH STUFF OURSELVES
        level = [ [platforms.GRASS_LEFT, 500, 500],
                  [platforms.GRASS_MIDDLE, 570, 500],
                  [platforms.GRASS_RIGHT, 640, 500],
                  [platforms.GRASS_LEFT, 800, 400],
                  [platforms.GRASS_MIDDLE, 870, 400],
                  [platforms.GRASS_RIGHT, 940, 400],
                  [platforms.GRASS_LEFT, 1000, 500],
                  [platforms.GRASS_MIDDLE, 1070, 500],
                  [platforms.GRASS_RIGHT, 1140, 500],
                  [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                  [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                  [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
                  ]


        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        '''setup_enemies(self)

        def setup_enemies(self):
            #Creates all the enemies and stores them in a list of lists.
                goomba0 = enemies.Goomba()
                goomba1 = enemies.Goomba()
                goomba2 = enemies.Goomba()
                goomba3 = enemies.Goomba()
                goomba4 = enemies.Goomba(193)
                goomba5 = enemies.Goomba(193)
                goomba6 = enemies.Goomba()
                goomba7 = enemies.Goomba()
                goomba8 = enemies.Goomba()
                goomba9 = enemies.Goomba()
                goomba10 = enemies.Goomba()
                goomba11 = enemies.Goomba()
                goomba12 = enemies.Goomba()
                goomba13 = enemies.Goomba()
                goomba14 = enemies.Goomba()
                goomba15 = enemies.Goomba()

                koopa0 = enemies.Koopa()

                enemy_group1 = pg.sprite.Group(goomba0)
                enemy_group2 = pg.sprite.Group(goomba1)
                enemy_group3 = pg.sprite.Group(goomba2, goomba3)
                enemy_group4 = pg.sprite.Group(goomba4, goomba5)
                enemy_group5 = pg.sprite.Group(goomba6, goomba7)
                enemy_group6 = pg.sprite.Group(koopa0)
                enemy_group7 = pg.sprite.Group(goomba8, goomba9)
                enemy_group8 = pg.sprite.Group(goomba10, goomba11)
                enemy_group9 = pg.sprite.Group(goomba12, goomba13)
                enemy_group10 = pg.sprite.Group(goomba14, goomba15)

                self.enemy_group_list = [enemy_group1,
            	                         enemy_group2,
            	                         enemy_group3,
            	                         enemy_group4,
            	                         enemy_group5,
            	                         enemy_group6,
            	                         enemy_group7,
            	                         enemy_group8,
            	                         enemy_group9,
            	                         enemy_group10]'''

# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("background_2.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -1000

        # Array with type of platform, and x, y location of the platform.
	# __ REPLACE THESE ___
        level = [ [platforms.STONE_PLATFORM_LEFT, 500, 550],
                  [platforms.STONE_PLATFORM_MIDDLE, 570, 550],
                  [platforms.STONE_PLATFORM_RIGHT, 640, 550],
                  [platforms.GRASS_LEFT, 800, 400],
                  [platforms.GRASS_MIDDLE, 870, 400],
                  [platforms.GRASS_RIGHT, 940, 400],
                  [platforms.GRASS_LEFT, 1000, 500],
                  [platforms.GRASS_MIDDLE, 1070, 500],
                  [platforms.GRASS_RIGHT, 1140, 500],
                  [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                  [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                  [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
                  ]


        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        '''def setup_enemies(self):
            #Creates all the enemies and stores them in a list of lists.
                goomba0 = enemies.Goomba()
                goomba1 = enemies.Goomba()
                goomba2 = enemies.Goomba()
                goomba3 = enemies.Goomba()
                goomba4 = enemies.Goomba(193)
                goomba5 = enemies.Goomba(193)
                goomba6 = enemies.Goomba()
                goomba7 = enemies.Goomba()
                goomba8 = enemies.Goomba()
                goomba9 = enemies.Goomba()
                goomba10 = enemies.Goomba()
                goomba11 = enemies.Goomba()
                goomba12 = enemies.Goomba()
                goomba13 = enemies.Goomba()
                goomba14 = enemies.Goomba()
                goomba15 = enemies.Goomba()

                koopa0 = enemies.Koopa()

                enemy_group1 = pg.sprite.Group(goomba0)
                enemy_group2 = pg.sprite.Group(goomba1)
                enemy_group3 = pg.sprite.Group(goomba2, goomba3)
                enemy_group4 = pg.sprite.Group(goomba4, goomba5)
                enemy_group5 = pg.sprite.Group(goomba6, goomba7)
                enemy_group6 = pg.sprite.Group(koopa0)
                enemy_group7 = pg.sprite.Group(goomba8, goomba9)
                enemy_group8 = pg.sprite.Group(goomba10, goomba11)
                enemy_group9 = pg.sprite.Group(goomba12, goomba13)
                enemy_group10 = pg.sprite.Group(goomba14, goomba15)

                self.enemy_group_list = [enemy_group1,
            	                         enemy_group2,
            	                         enemy_group3,
            	                         enemy_group4,
            	                         enemy_group5,
            	                         enemy_group6,
            	                         enemy_group7,
            	                         enemy_group8,
            	                         enemy_group9,
            	                         enemy_group10] '''
