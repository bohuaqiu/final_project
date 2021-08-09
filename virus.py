import pygame
import math
import os
import random

WIN_WIDTH = 1024
WIN_HEIGHT = 600
FPS = 120
virus_image = pygame.image.load(os.path.join("images", "virus.png"))
#BULLET_IMAGE = pygame.image.load(os.path.join("bullet.png"))

class Virus:
    def __init__(self):
        self.image = pygame.transform.scale(virus_image, (100, 100))
        #self.bullet_image = pygame.transform.scale(BULLET_IMAGE, (10, 10))
        self.rect = self.image.get_rect()
        #self.x, self.y = self.rect.center
        self.health = 300
        self.max_health = 300
        self.dmg=10
        self.dx = -2
        self.dy = 1
        self.start = 1
        self.atk_cd=0
        self.atk_max_cd=60
        self.shoot_cd = 0
        self.bullet_dx = -10
        self.pass_dmg=False
    
    def move(self):
        """
        敵人移動路徑
        """
        if self.start == 1:
            self.dx = -2
            self.dy = random.randint(-1,1)
            self.rect.centerx,self.rect.centery = (WIN_WIDTH - 100, random.randint(0, WIN_HEIGHT - 100))
            self.start = 0
        if self.rect.centerx >= WIN_WIDTH - 100:
            self.dx = random.randint(-3,-2)
            
        if self.rect.centerx <= 0:
            self.dx = random.randint(2,3)
            
        if self.rect.centery >= WIN_HEIGHT - 100:
            self.dy = random.randint(-3,-2)
            
        if self.rect.centery <= 200 :
            self.dy = random.randint(2,3)
            
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        
    def is_cd(self):
        if self.atk_cd<self.atk_max_cd:
            self.atk_cd+=1
            return True
        else:
            return False
        
    def shoot(self, x, y):
        if self.shoot_cd == 120:
            self.shoot_cd = 0
            
    def attack(self,player):
        if(player.get_attack(self.rect.center) and self.is_cd()==False):
            player.get_hurt(self.dmg)
            self.atk_cd=0
        
         
    def is_hitted(self,bullet_pos):
        if self.rect.collidepoint(bullet_pos):
            return True
        else:
            return False    
            
        self.self.shoot_cd += 1
    def get_hurt(self,dmg):
        self.health-=dmg
        self.pass_dmg=True
        

    def draw(self, win):
        win.blit(self.image,self.rect)
class Virusgroup:
    def __init__(self):
        self.font = pygame.font.SysFont("comicsans", 30)
        self.campaign_count = 0
        self.campaign_max_count = 30
        self.__reserved_members = []
        self.__expedition = []
        self.kill_amount = 0
        

    def draw(self, win):
        for en in self.__expedition:
            win.blit(en.image, (en.rect.centerx,en.rect.centery))
            current_health_ratio = en.health / en.max_health
            pygame.draw.rect(win, (255, 0, 0), [en.rect.centerx + 20, en.rect.centery - 10, 65, 10])
            pygame.draw.rect(win, (0, 255, 0), [en.rect.centerx + 20, en.rect.centery - 10, 65 * current_health_ratio, 10])
        text = self.font.render(f"Kill: {self.kill_amount}", True, (255, 255, 255)) # 畫出擊殺病毒數量
        win.blit(text, (800, 15))
    def campaign(self):
        """
        Enemy go on an expedition.
        """
        if self.campaign_count > self.campaign_max_count and self.__reserved_members:
            self.__expedition.append(self.__reserved_members.pop())
            self.campaign_count = 0
        else:
            self.campaign_count += 1

    def add(self, num):
        """
        Generate the enemies for next wave
        """
        self.__reserved_members = [Virus() for _ in range(num)]

    def get(self):
        """
        Get the enemy list
        """
        return self.__expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.__reserved_members or self.__expedition else True
    def update(self,player):
        for en in self.__expedition:
             en.is_cd()
             en.attack(player)
             if(en.health<=0):
                self.__expedition.remove(en)
                self.kill_amount += 1         # 擊殺病毒數量
        
    def touch(self, virus):
        return self.__expedition
    
    
    
        