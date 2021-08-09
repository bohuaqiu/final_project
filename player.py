import pygame
import os
from setting import WIN_WIDTH,RED,GREEN

pygame.init()
PLAYER_IMAGE = pygame.image.load(os.path.join("images", "1.png"))
PLAYER_IMAGE_L = pygame.transform.flip(PLAYER_IMAGE,True,False)

class Player:
    def __init__(self):
        self.image=pygame.transform.scale(PLAYER_IMAGE,(150,200))
        self.rect=self.image.get_rect()
        self.x=500 #玩家的初始位置
        self.y=450
        self.rect.center=(self.x,self.y)
        self.hp=100
        self.max_hp=100
        self.jumping=False#用於判斷玩家是否在跳躍中
        self.face_to_right=True
        self.jump_time=0
    def draw(self, win):
        '''
        輸出玩家的血量與圖像
        '''
        win.blit(self.image,self.rect)
        pygame.draw.rect(win,GREEN,[400,20,2*self.hp,20])
        pygame.draw.rect(win,RED,[400+2*self.hp,20,2*(self.max_hp-self.hp),20])
    def is_jumping(self): #進行跳躍的function
        '''
        跳躍的總時間為51幀
        前半段時間位置會逐漸升高
        後半段時間位置逐漸降低
        '''
        if(self.jumping):
            if(self.jump_time<=25):
                self.y-=4   
            else:
                self.y+=4
            self.jump_time+=1    
            if(self.jump_time==51):
                self.jumping = False
                self.jump_time=0 #跳躍完成后重置跳躍時間
    def is_down(self,down):#判斷是否為蹲下
        if(self.jumping==False): 
            if(down):
                self.y=480
            else:
                self.y=450
    def face_to(self):#判斷玩家當前的面朝向，會跟換圖像
        if (self.face_to_right):
            self.image=pygame.transform.scale(PLAYER_IMAGE,(150,200))
        else:
            self.image=pygame.transform.scale(PLAYER_IMAGE_L,(150,200))

    
class Player_action: #控制玩家的動作
    def __init__(self):
        self.down=False
        self.player=Player()
        
    def update(self):
        self.player.face_to()
        self.player.is_down(self.down)
        self.player.is_jumping()
        self.player.rect.centerx=self.player.x
        self.player.rect.centery=self.player.y
        
    def draw(self,win):
        self.player.draw(win)      
        
    def move_L(self): #往左移動
        if(self.player.x>=10):
            self.player.x-=2 
            
    def move_R(self): #往右移動
        if(self.player.x<=WIN_WIDTH-10):
            self.player.x+=2  
            
    def jump(self): #跳躍
        self.player.jumping =True
        
    def turn_R(self): #turn_R,turn_l可改變面朝向，但很少用
        self.player.face_to_right=True

    def turn_L(self):
        self.player.face_to_right=False    
        
    def shot(self,x,y): #射擊時會改變面朝向
        if((x-self.player.x)>=0):
            self.player.face_to_right=True
        else:
            self.player.face_to_right=False
            
    def get_attack(self,virus_pos): #判斷玩家是否收到病毒攻擊，virus_pos為病毒的位置
        if self.player.rect.collidepoint(virus_pos):
            return True
        else:
            return False    
            
    def get_hurt(self,dmg):
        self.player.hp-=dmg#根據病毒傷害扣除血量
    
    def get_pos_x(self):
        return self.player.x
    
    def get_pos_y(self):
        return self.player.y
    
    def get(self):
        return self.player
    