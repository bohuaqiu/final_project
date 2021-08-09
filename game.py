import pygame
import os
from player import Player_action
from setting import WIN_HEIGHT, WIN_WIDTH,FPS
from bullet import BulletGroup
from virus import Virusgroup
# load image
BACKGROUND_IMAGE_1 = pygame.image.load(os.path.join("images", "level_1_background.png"))
BACKGROUND_IMAGE_2 = pygame.image.load(os.path.join("images", "level_2_background.png"))
BACKGROUND_IMAGE_3 = pygame.image.load(os.path.join("images", "level_3_background.png"))

class Game:
    def __init__(self):
        self.lose = pygame.transform.scale(pygame.image.load(os.path.join("images", "lose.png")), (WIN_WIDTH, WIN_HEIGHT))
        self.success = pygame.transform.scale(pygame.image.load(os.path.join("images", "win.png")), (WIN_WIDTH, WIN_HEIGHT))
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.bg_image = pygame.transform.scale(BACKGROUND_IMAGE_1, (WIN_WIDTH, WIN_HEIGHT))
        self.player = Player_action()
        self.bullet = BulletGroup()
        self.virus = Virusgroup()
        self.virus_spawn_amount = 5 # 增加敵人
    def run(self):
        self.quit_game=False
        while not self.quit_game:
            pygame.time.Clock().tick(FPS)
            pl=self.player.get()
            if self.virus.is_empty():
                self.virus.add(self.virus_spawn_amount)
                self.virus_spawn_amount += 5
            if pl.hp<=0 :
                pygame.init()
                self.win.blit(self.lose, (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                       self.quit_game = True    
                pygame.display.update()  
            elif self.virus.kill_amount >= 100:# if擊殺病毒數量超過x隻 
                 pygame.init()
                 self.win.blit(self.success, (0, 0))# success
                 for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_game = True                
                 pygame.display.update()
            else:
                self.draw()
                self.quit_game=self.update()
            
            
                
    def draw(self):
        # draw background
        self.win.blit(self.bg_image, (0, 0))
        # draw player
        self.player.draw(self.win)
        self.virus.draw(self.win)
        self.bullet.draw(self.win)
        pygame.display.update()

    def update(self):
        pygame.init()
        game_quit = False
        # event loop
        while not game_quit:
            # virus
            self.virus.campaign()                                    
            for en in self.virus.get():
                en.move()
                en.draw(self.win)           
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_quit = True
                    return game_quit
                # player press action
                if event.type == pygame.KEYDOWN:
                    if(event.key == pygame.K_w):
                        self.player.jump()
                key_pressed= pygame.key.get_pressed()   #因為考慮同時按下三個按鍵的情況，所以設置三個key_pressed     
                key_pressed_2= pygame.key.get_pressed()
                key_pressed_3 = pygame.key.get_pressed()
                if (key_pressed[pygame.K_u] or key_pressed_2[pygame.K_u] or key_pressed_3[pygame.K_u]):
                    self.player.turn_L()
                elif (key_pressed[pygame.K_i] or key_pressed_2[pygame.K_i] or key_pressed_3[pygame.K_i]):
                      self.player.turn_R()                
                if (key_pressed[pygame.K_a] or key_pressed_2[pygame.K_a] or key_pressed_3[pygame.K_a]):
                    self.player.move_L()
                elif (key_pressed[pygame.K_d] or key_pressed_2[pygame.K_d] or key_pressed_3[pygame.K_d]):
                      self.player.move_R()
                if(key_pressed[pygame.K_LSHIFT] or key_pressed_2[pygame.K_LSHIFT] or key_pressed_3[pygame.K_LSHIFT]):
                    self.player.down=True
                else:
                    self.player.down=False
                #if (key_pressed[pygame.K_n] or key_pressed_2[pygame.K_n] or key_pressed_3[pygame.K_n]):
                     
                # player click action
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.shot(mouse_x,mouse_y)
                    self.bullet.add(self.player.get_pos_x(),self.player.get_pos_y(),mouse_x,mouse_y,self.virus)  
                elif (key_pressed[pygame.K_SPACE] or key_pressed_2[pygame.K_SPACE] or key_pressed_3[pygame.K_SPACE]):
                     self.player.shot(mouse_x,mouse_y)
                     self.bullet.alcohol_shot(self.player.get_pos_x(),self.player.get_pos_y(),mouse_x,mouse_y,self.virus)                      
            self.bullet.update(self.virus)
            self.virus.update(self.player)
            self.player.update()    
            return game_quit

    