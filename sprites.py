import pygame 
from Variabler import *
import math as math
import random as random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.carrying_sheep = None  
        self.game.sheeps_delivered = 0

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = "down"
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(32, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(64, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(96, 0, self.width, self.height)
                           ]

        self.left_animations = [self.game.character_spritesheet.get_sprite(0, 32, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(32, 32, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(64, 32, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(96, 32, self.width, self.height)]

        self.up_animations = [self.game.character_spritesheet.get_sprite(0, 96, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(32, 96, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(64, 96, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(96, 96, self.width, self.height)]

        self.right_animations = [self.game.character_spritesheet.get_sprite(0, 64, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(32, 64, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(64, 64, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(96, 64, self.width, self.height)]
    
    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()
        self.collide_sheep()
        self.collide_goal()
        
        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")

        if self.carrying_sheep:
            self.carrying_sheep.rect.center = self.rect.center

        self.x_change = 0
        self.y_change = 0
    
    def collide_sheep(self):
        hits = pygame.sprite.spritecollide(self, self.game.sheeps, False)
        if hits and self.game.keys[pygame.K_e]:
            if self.carrying_sheep is None:
                self.carrying_sheep = hits[0]
                self.carrying_sheep.is_carried = True
                self.carrying_sheep.rect.center = self.rect.center
        
    def drop_sheep(self):  
        if self.carrying_sheep:
            self.carrying_sheep.rect.x = int(self.rect.x / TILESIZE) * TILESIZE
            self.carrying_sheep.rect.y = int(self.rect.y / TILESIZE) * TILESIZE
            self.carrying_sheep.is_carried = False
            self.carrying_sheep.animation_loop = 1
            self.carrying_sheep = None
            
    
    def collide_goal(self):
        if self.carrying_sheep:
            if pygame.sprite.spritecollide(self, self.game.goal_tiles, False):
                self.carrying_sheep.kill()
                self.carrying_sheep = None
                self.game.sheeps_delivered += 1

    def draw_text(self, surface):
        font = pygame.font.Font("Iceberg-Regular.ttf", 24)
        text = font.render(f"Sauer levert: {self.sheeps_delivered}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.top - 10))
        surface.blit(text, text_rect)
    
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = "left"
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = "right"
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = "up"
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = "down"

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.game.playing = False
            self.game.game_over()
            self.kill()

    def collide_blocks(self,direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        if self.facing == "down": 
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 32, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1
        
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 64, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        
        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 96, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1



class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(["left", "right", "up", "down"])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7,100)

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.enemy_spritesheet.get_sprite(0, 32, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(32, 32, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(64, 32, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(96, 32, self.width, self.height)]

    
        self.left_animations = [self.game.enemy_spritesheet.get_sprite(0, 64, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(32, 64, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(64, 64, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(96, 64, self.width, self.height)]
        
        self.right_animations = [self.game.enemy_spritesheet.get_sprite(0, 96, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(32, 96, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(64, 96, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(96, 96, self.width, self.height)]
                            
        self.up_animations = [self.game.enemy_spritesheet.get_sprite(0, 128, self.width, self.height),
                              self.game.enemy_spritesheet.get_sprite(32, 128, self.width, self.height),
                              self.game.enemy_spritesheet.get_sprite(64, 128, self.width, self.height),
                              self.game.enemy_spritesheet.get_sprite(96, 128, self.width, self.height)]

    def update(self):
        old_x = self.rect.x
        old_y = self.rect.y
        
        self.movement()
        
        self.rect.x += self.x_change
        block_hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if block_hits:
            self.rect.x = old_x
            self.facing = random.choice(["up", "down"])
            self.movement_loop = 0
        
        self.rect.y += self.y_change
        block_hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if block_hits:
            self.rect.y = old_y
            self.facing = random.choice(["left", "right"])
            self.movement_loop = 0
        
        self.animate()
        self.x_change = 0
        self.y_change = 0


        

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

                self.facing = random.choice(["up", "down", "left", "right"])

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

                self.facing = random.choice(["up", "down", "left", "right"])
        

    def movement(self):
        if self.facing == "left":
            self.x_change = -ENEMY_SPEED
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits or self.movement_loop <= -self.max_travel:
                self.facing = random.choice(["right", "up", "down"])
                self.movement_loop = 0
            else:
                self.movement_loop -= 1

        elif self.facing == "right":
            self.x_change = ENEMY_SPEED
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits or self.movement_loop >= self.max_travel:
                self.facing = random.choice(["left", "up", "down"])
                self.movement_loop = 0
            else:
                self.movement_loop += 1

        elif self.facing == "up":
            self.y_change = -ENEMY_SPEED
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits or self.movement_loop <= -self.max_travel:
                self.facing = random.choice(["down", "left", "right"])
                self.movement_loop = 0
            else:
                self.movement_loop -= 1

        elif self.facing == "down":
            self.y_change = ENEMY_SPEED
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits or self.movement_loop >= self.max_travel:
                self.facing = random.choice(["up", "left", "right"])
                self.movement_loop = 0
            else:
                self.movement_loop += 1


    def animate(self):
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(0, 32, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1
        
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(0, 64, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(0, 96, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(0, 0, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(0, 32, self.height, self.width)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Sheep(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = SHEEP_LAYER
        self.groups = self.game.all_sprites, self.game.sheeps
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(["left", "right", "up", "down"])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(20, 280)

        self.image = self.game.sheep_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.is_carried = False

        self.down_animations = [
            self.game.sheep_spritesheet.get_sprite(0, 0, self.width, self.height),
            self.game.sheep_spritesheet.get_sprite(32, 0, self.width, self.height),
            self.game.sheep_spritesheet.get_sprite(64, 0, self.width, self.height)
        ]

        self.left_animations = [
            self.game.sheep_spritesheet.get_sprite(0, 32, self.width, self.height),
            self.game.sheep_spritesheet.get_sprite(32, 32, self.width, self.height),
            self.game.sheep_spritesheet.get_sprite(64, 32, self.width, self.height)
        ]

        self.right_animations = [
            self.game.sheep_spritesheet.get_sprite(0, 64, self.width, self.height),
            self.game.sheep_spritesheet.get_sprite(32, 64, self.width, self.height),
            self.game.sheep_spritesheet.get_sprite(64, 64, self.width, self.height)
        ]

        self.up_animations = [
            self.game.sheep_spritesheet.get_sprite(0, 96, self.width, self.height),
            self.game.sheep_spritesheet.get_sprite(32, 96, self.width, self.height),
            self.game.sheep_spritesheet.get_sprite(64, 96, self.width, self.height)
        ]

    def update(self):
        old_x = self.rect.x
        old_y = self.rect.y
        
        if not self.is_carried:
            self.movement()
        
        self.rect.x += self.x_change
        block_hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if block_hits:
            self.rect.x = old_x
            self.facing = random.choice(["up", "down"])
            self.movement_loop = 0
        
        self.rect.y += self.y_change
        block_hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if block_hits:
            self.rect.y = old_y
            self.facing = random.choice(["left", "right"])
            self.movement_loop = 0
        
        self.animate()
        self.x_change = 0
        self.y_change = 0


    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                self.facing = random.choice(["up", "down", "left", "right"])

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                self.facing = random.choice(["up", "down", "left", "right"])

    def movement(self):
        if self.facing == "left":
            self.x_change = -ENEMY_SPEED
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits or self.movement_loop <= -self.max_travel:
                self.facing = random.choice(["right", "up", "down"])
                self.movement_loop = 0
            else:
                self.movement_loop -= 1

        elif self.facing == "right":
            self.x_change = ENEMY_SPEED
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits or self.movement_loop >= self.max_travel:
                self.facing = random.choice(["left", "up", "down"])
                self.movement_loop = 0
            else:
                self.movement_loop += 1

        elif self.facing == "up":
            self.y_change = -ENEMY_SPEED
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits or self.movement_loop <= -self.max_travel:
                self.facing = random.choice(["down", "left", "right"])
                self.movement_loop = 0
            else:
                self.movement_loop -= 1

        elif self.facing == "down":
            self.y_change = ENEMY_SPEED
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits or self.movement_loop >= self.max_travel:
                self.facing = random.choice(["up", "left", "right"])
                self.movement_loop = 0
            else:
                self.movement_loop += 1

    def animate(self):
        """ Bytter bilde basert på retning og loop """
        if self.facing == "left":
            anim_list = self.left_animations
        elif self.facing == "right":
            anim_list = self.right_animations
        elif self.facing == "up":
            anim_list = self.up_animations
        elif self.facing == "down":
            anim_list = self.down_animations

        index = int(self.animation_loop) % len(anim_list)
        self.image = anim_list[index]

        self.animation_loop += 0.1
        if self.animation_loop >= 4:
            self.animation_loop = 1


        
class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(0, 0, self.height, self.width)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Goal_tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.goal_tiles
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(32, 0, self.height, self.width)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
class Button:
    def __init__(self, x, y, width, height, color, hover_color, text, font_size):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font = pygame.font.Font("Iceberg-Regular.ttf", font_size)
        self.text_color = WHITE
        self.hover_text_color = GRAY
        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)

        self.update_text(self.text_color)

    def update_text(self, color):
        """Oppdaterer knappeteksten med riktig farge"""
        text_surface = self.font.render(self.text, True, color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.image.fill(self.color)
        self.image.blit(text_surface, (self.rect.width // 2 - text_rect.width // 2, 
                                       self.rect.height // 2 - text_rect.height // 2))

    def is_hovered(self, mouse_pos):
        """Sjekker om musen er over knappen"""
        return self.rect.collidepoint(mouse_pos)

    def is_pressed(self, mouse_pos, mouse_pressed):
        """Sjekker om knappen trykkes"""
        return self.is_hovered(mouse_pos) and mouse_pressed[0]

    def draw(self, screen, mouse_pos):
        """Tegner knappen med riktig farge basert på om musen er over"""
        if self.is_hovered(mouse_pos):
            self.update_text(self.hover_text_color)
        else:
            self.update_text(self.text_color)

        screen.blit(self.image, self.rect.topleft)


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
    
        self.animation_loop = 0

        self.image = self.game.attack_spritesheet.get_sprite(0,0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        self.down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing
        
        if direction == "up":
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == "down":
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == "left":
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
                
        if direction == "right":
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()