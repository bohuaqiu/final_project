import pygame
import os
from game import Game
from setting import WIN_WIDTH, WIN_HEIGHT, FPS, GRAY

pygame.init()
pygame.mixer.init()


class StartMenu:
    def __init__(self):
        # win
        self.menu_win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        # background
        self.bg = pygame.transform.scale(pygame.image.load(os.path.join("images", "start_menu.png")), (WIN_WIDTH, WIN_HEIGHT))
        # button
        self.start_btn = Buttons(473, 416, 94, 94)  # x, y, width, height
        self.sound_btn = Buttons(22.5, 12.5, 55, 55)
        self.mute_btn = Buttons(92.5, 12.5, 55, 55)
        self.music_buttons = [self.start_btn,self.sound_btn,self.mute_btn]

    def play_music(self):
        pygame.mixer.music.load("Under_The_Radar.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def menu_run(self):
        run = True
        clock = pygame.time.Clock()
        pygame.display.set_caption("Drive Out The Virus")
        self.play_music()
        while run:
            clock.tick(FPS)
            self.menu_win.blit(self.bg, (0, 0))
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # check if hit start btn
                    if self.start_btn.clicked(x, y):
                        #self.sound.play()
                        game = Game()
                        game.run()
                        run = False
                        
                    if self.mute_btn.clicked(x, y):         # 當 mute 這個 button 被按下的時候，將音樂停止
                         pygame.mixer.music.pause()
                    elif self.sound_btn.clicked(x, y):      # 當 sound 這個 button 被按下的時候，播放音樂
                        pygame.mixer.music.unpause()

            for btn in self.music_buttons:
                btn.create_frame(x, y)
                btn.draw_frame(self.menu_win)


            pygame.display.update()
        pygame.quit()


class Buttons:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.frame = False
        self.radius = (width/2)+(width/20)
        self.x_pos = x + (width/2)
        self.y_pos = y + (height/2)

    def clicked(self, x: int, y: int) -> bool:
        if self.rect.collidepoint(x, y):
            return True
        return False
    
    def create_frame(self, x: int, y: int):
        """if cursor position is on the button, create button frame"""
        if self.clicked(x, y):
            self.frame = True
        else:
            self.frame = False


    def draw_frame(self, win):
        if self.frame == True:
            pygame.draw.circle(win, GRAY, (self.x_pos, self.y_pos), self.radius, 5)

