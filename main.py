import pygame
from sprites import *
from Variabler import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font("Iceberg-Regular.ttf", 32)

        self.character_spritesheet = Spritesheet("img/characters.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
        self.enemy_spritesheet = Spritesheet("img/enemy.png")
        # self.intro_background = pygame.image.load("")


    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self,j,i)
                if column == "B":
                    Block(self,j,i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "P":
                    Player(self,j,i)

    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap()


    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):

        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False
    
    def game_over(self):
        pass
    def intro_screen(self): 
        pass
        # intro = True

        # title = self.font.render("Manic Mansion", True, BLACK)
        # title_rect = title.get_rect(x=10, y=10)

        # play_button = Button(10, 50, 100, 50, WHITE, BLACK, "Play", 32)

        # while intro:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             intro = False
        #             self.running = False

        #     mouse_pos = pygame.mouse.get_pos()
        #     mouse_pressed = pygame.mouse.get_pressed()

        #     if play_button.is_pressed(mouse_pos, mouse_pressed):
        #         intro = False

        #     self.screen.blit(self.intro_background,(0,0))
        #     self.screen.blit(title, title_rect)
        #     self.screen.blit(play_button.image, play_button.rect)
        #     self.clock.tick(FPS)
        #     pygame.display.update()
            

    def update(self):
        self.all_sprites.update()

spill = Game()
spill.intro_screen()
spill.new()
while spill.running:
    spill.main()

pygame.quit()
sys.exit()