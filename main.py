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
        self.sheeps_delivered = 0


        self.character_spritesheet = Spritesheet("img/characters.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
        self.enemy_spritesheet = Spritesheet("img/enemy.png")
        self.attack_spritesheet = Spritesheet("img/attack.png")
        self.intro_background = pygame.image.load("img/intro_background.png")
        self.go_background = pygame.image.load("img/intro_background.png")
        self.sheep_spritesheet = Spritesheet("img/sheep.jpg")
        self.keys = pygame.key.get_pressed()



    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self,j,i)
                if column == "B":
                    Block(self,j,i)
                if column == "E":
                    Enemy(self,j,i)
                if column == "P":
                    self.player = Player(self,j,i)
                if column == "S":
                    Sheep(self,j,i)
                if column == "G":
                    Goal_tile(self,j,i)



    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.sheeps = pygame.sprite.LayeredUpdates()
        self.goal_tiles = pygame.sprite.LayeredUpdates()

        self.createTilemap()


    def events(self):
        self.keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e: # Drop sheep with "e"
                    self.player.drop_sheep()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == "up":
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == "down":
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == "left":
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == "right":
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)
        if self.sheeps_delivered == 5:
            self.winning_screen()



    def winning_screen(self):
        text = self.font.render("Gratulerer, du vant!", True, BLACK)
        text_rect = text.get_rect(x=185, y=100)
        
        restart_button = Button(255, 200, 120, 50, BLACK, BLACK, "Restart", 32)
        quit_button = Button(265, 350, 100, 50, BLACK, BLACK, "Quit", 32)
        tutorial_button = Button(255, 270, 120, 60, BLACK, BLACK, "Tutorial", 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            if tutorial_button.is_pressed(mouse_pos, mouse_pressed):
                self.from_win_tutorial_screen()
            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                self.running = False
                pygame.quit()
                sys.exit()

            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            restart_button.draw(self.screen, mouse_pos)
            tutorial_button.draw(self.screen, mouse_pos)
            quit_button.draw(self.screen, mouse_pos)
            self.clock.tick(FPS)
            pygame.display.update()

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
    
    def game_over(self):
        self.all_sprites.empty()
        self.blocks.empty()
        self.enemies.empty()
        self.attacks.empty()
        self.sheeps.empty()
        self.goal_tiles.empty()

        text = self.font.render("Game Over", True, BLACK)
        text_rect = text.get_rect(x=244, y=100)
        
        restart_button = Button(255, 200, 120, 50, BLACK, BLACK, "Restart", 32)
        quit_button = Button(265, 350, 100, 50, BLACK, BLACK, "Quit", 32)
        tutorial_button = Button(255, 270, 120, 60, BLACK, BLACK, "Tutorial", 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            if tutorial_button.is_pressed(mouse_pos, mouse_pressed):
                self.from_dead_tutorial_screen()
            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                self.running = False
                pygame.quit()
                sys.exit()

            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            restart_button.draw(self.screen, mouse_pos)
            tutorial_button.draw(self.screen, mouse_pos)
            quit_button.draw(self.screen, mouse_pos)
            self.clock.tick(FPS)
            pygame.display.update()


    def intro_screen(self): 
        intro = True

        title = self.font.render("Manic Mansion", True, BLACK)
        title_rect = title.get_rect(x=220, y=100)

        play_button = Button(265, 200, 100, 50, BLACK, BLACK, "Play", 32)
        tutorial_button = Button(255, 270, 120, 60, BLACK, BLACK, "Tutorial", 32)
        quit_button = Button(265, 350, 100, 50, BLACK, BLACK, "Quit", 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            if tutorial_button.is_pressed(mouse_pos, mouse_pressed):
                self.tutorial_screen()
            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                self.running = False
                pygame.quit()
                sys.exit()

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)

            # Bruk den nye `draw()`-metoden for å tegne knappene med hover-effekt
            play_button.draw(self.screen, mouse_pos)
            tutorial_button.draw(self.screen, mouse_pos)
            quit_button.draw(self.screen, mouse_pos)

            self.clock.tick(FPS)
            pygame.display.update()


    def tutorial_screen(self):
        tutorial = True

        tutorial_title = self.font.render("Tutorial", True, BLACK)
        tutorial_title_rect = tutorial_title.get_rect(center=(WIN_WIDTH // 2, 100))

        tutorial_text = (
            "Dette spillet går ut på at du skal gå rundt på kartet "
            "og samle inn sauer og ta dem med til et trygt sted. "
            "På veien må du unngå å bli drept av zombier. Likevel, "
            "kan du velge å drepe zombiene, dersom du er dristig nok, "
            "ved å trykke på 'spacebar'. Du plukker opp sauer ved å trykke 'e' og "
            "de blir sluppet løs med en gang du beveger deg innenfor det brune feltet. "
            "For å bevege deg bruker du piltastene"
        )

        words = tutorial_text.split()
        lines = []
        line = ""

        for word in words:
            test_line = line + word + " "
            if self.font.size(test_line)[0] < WIN_WIDTH - 40:
                line = test_line
            else:
                lines.append(line)
                line = word + " "

        lines.append(line)

        text_surfaces = [self.font.render(line, True, BLACK) for line in lines]
        text_rects = [text.get_rect(center=(WIN_WIDTH // 2, 150 + i * 30)) for i, text in enumerate(text_surfaces)]

        back_button = Button(10, 420, 100, 50, BLACK, BLACK, "Back", 32)

        while tutorial:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    tutorial = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if back_button.is_pressed(mouse_pos, mouse_pressed):
                tutorial = False
                self.intro_screen()

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(tutorial_title, tutorial_title_rect)

            for text_surface, text_rect in zip(text_surfaces, text_rects):
                self.screen.blit(text_surface, text_rect)

            # Tegner back-knappen med hover-effekt
            back_button.draw(self.screen, mouse_pos)

            self.clock.tick(FPS)
            pygame.display.update()

    def from_dead_tutorial_screen(self):
        tutorial = True

        tutorial_title = self.font.render("Tutorial", True, BLACK)
        tutorial_title_rect = tutorial_title.get_rect(center=(WIN_WIDTH // 2, 100))

        tutorial_text = (
            "Dette spillet går ut på at du skal gå rundt på kartet "
            "og samle inn sauer og ta dem med til et trygt sted. "
            "På veien må du unngå å bli drept av zombier. Likevel, "
            "kan du velge å drepe zombiene, dersom du er dristig nok, "
            "ved å trykke på 'spacebar'.Du plukker opp sauer ved å trykke 'e' og "
            "de blir sluppet løs med en gang du beveger deg innenfor det brune feltet. "
            "For å bevege deg bruker du piltastene"
        )

        words = tutorial_text.split()
        lines = []
        line = ""

        for word in words:
            test_line = line + word + " "
            if self.font.size(test_line)[0] < WIN_WIDTH - 40:
                line = test_line
            else:
                lines.append(line)
                line = word + " "

        lines.append(line)

        text_surfaces = [self.font.render(line, True, BLACK) for line in lines]
        text_rects = [text.get_rect(center=(WIN_WIDTH // 2, 150 + i * 30)) for i, text in enumerate(text_surfaces)]

        back_button = Button(10, 420, 100, 50, BLACK, BLACK, "Back", 32)

        while tutorial:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    tutorial = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if back_button.is_pressed(mouse_pos, mouse_pressed):
                tutorial = False
                self.game_over()

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(tutorial_title, tutorial_title_rect)

            for text_surface, text_rect in zip(text_surfaces, text_rects):
                self.screen.blit(text_surface, text_rect)

            # Tegner back-knappen med hover-effekt
            back_button.draw(self.screen, mouse_pos)

            self.clock.tick(FPS)
            pygame.display.update()

    def from_win_tutorial_screen(self):
        tutorial = True

        tutorial_title = self.font.render("Tutorial", True, BLACK)
        tutorial_title_rect = tutorial_title.get_rect(center=(WIN_WIDTH // 2, 100))

        tutorial_text = (
            "Dette spillet går ut på at du skal gå rundt på kartet "
            "og samle inn sauer og ta dem med til et trygt sted. "
            "På veien må du unngå å bli drept av zombier. Likevel, "
            "kan du velge å drepe zombiene, dersom du er dristig nok, "
            "ved å trykke på 'spacebar'.Du plukker opp sauer ved å trykke 'e' og "
            "de blir sluppet løs med en gang du beveger deg innenfor det brune feltet. "
            "For å bevege deg bruker du piltastene"
        )

        words = tutorial_text.split()
        lines = []
        line = ""

        for word in words:
            test_line = line + word + " "
            if self.font.size(test_line)[0] < WIN_WIDTH - 40:
                line = test_line
            else:
                lines.append(line)
                line = word + " "

        lines.append(line)

        text_surfaces = [self.font.render(line, True, BLACK) for line in lines]
        text_rects = [text.get_rect(center=(WIN_WIDTH // 2, 150 + i * 30)) for i, text in enumerate(text_surfaces)]

        back_button = Button(10, 420, 100, 50, BLACK, BLACK, "Back", 32)

        while tutorial:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    tutorial = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if back_button.is_pressed(mouse_pos, mouse_pressed):
                tutorial = False
                self.winning_screen()

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(tutorial_title, tutorial_title_rect)

            for text_surface, text_rect in zip(text_surfaces, text_rects):
                self.screen.blit(text_surface, text_rect)

            # Tegner back-knappen med hover-effekt
            back_button.draw(self.screen, mouse_pos)

            self.clock.tick(FPS)
            pygame.display.update()

    def update(self):
        self.all_sprites.update()

spill = Game()
spill.intro_screen()
spill.new()
while spill.running:
    spill.main()

pygame.quit()
sys.exit()