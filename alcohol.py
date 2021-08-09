import pygame


class Alcohol_atk:
    def __init__(self):
        self.font = pygame.font.SysFont("comicsans", 30)
        self.charged=1500#初期提供100%充能
        self.cd=30
        self.max_cd=30
        self.max_charger=1500
        self.charger_time=300#一發酒精子彈所需的充能時間
        self.count_bullet=5#當前酒精子彈的數量
    def cd_count(self):
        '''
        用於計算酒精攻擊的冷卻與及充能，在BUlletGroup.update里進行呼叫
        '''
        self.count_bullet=int(self.charged/self.charger_time)
        if(self.charged<self.max_charger):
            self.charged+=1
        if(self.cd<self.max_cd):
            self.cd+=1
 
    def draw(self,win):
        text = self.font.render(f"Alcohol: {self.count_bullet}", True, (255, 255, 255))
        win.blit(text, (5, 15))
        pygame.draw.rect(win, (255,255,255), [5, 33, (self.charged%self.charger_time)/3, 5])        