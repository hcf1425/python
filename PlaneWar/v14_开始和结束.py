"""
   main 函数：主程序，写项目中的主要流程代码【逻辑代码】
"""
# 导入动态模块(.dll .pyd .so)
import pygame

from pygame.locals import *
import sys
import time
import random

# 定义常量
WINDOW_HEIGHT = 768
WINDOW_WIDTH = 512
enemy_list = []
score = 0
is_restart = False


class Map(object):

    def __init__(self, img_path, window):
        self.x = 0
        self.bg_img1 = pygame.image.load(img_path)
        self.bg_img2 = pygame.image.load(img_path)
        self.bg1_y = -WINDOW_HEIGHT
        self.bg2_y = 0
        self.window = window

    def move(self):

        if self.bg1_y > 0:
            self.bg1_y = -WINDOW_HEIGHT

        if self.bg2_y >= WINDOW_HEIGHT:
            self.bg2_y = 0

        self.bg1_y += 3
        self.bg2_y += 3

    def display(self):
        self.window.blit(self.bg_img1,(self.x,self.bg1_y))
        self.window.blit(self.bg_img2,(self.x,self.bg2_y))


# 定义英雄子弹
class HeroBullet(object):
    def __init__(self, image_path, x, y, window):
        self.img = pygame.image.load(image_path)
        self.x = x
        self.y = y
        self.window = window

    def display(self):
        self.window.blit(self.img, (self.x, self.y))

    def move(self):
        self.y -= 10

    def is_hit_enemy(self, enemy):
        # 判断是否碰撞
        if pygame.Rect.colliderect(
                pygame.Rect(self.x, self.y, 20, 31),
                pygame.Rect(enemy.x, enemy.y, 100, 68)
        ):
            return True
        else:
            return False


# 定义飞机基类
class BasePlane(object):
    def __init__(self, img_path, x, y, window):
        self.img = pygame.image.load(img_path)
        self.x = x
        self.y = y
        self.window = window

    def display(self):
        self.window.blit(self.img, (self.x, self.y))


# 定义英雄飞机类
class HeroPlane(BasePlane):
    def __init__(self, image_path, x, y, window):
        super().__init__(image_path, x, y, window)
        self.is_hited = False
        self.bullets = []

    def move_left(self):
        if self.x > 0:
           self.x -= 5

    def move_right(self):
        if self.x < WINDOW_WIDTH-120:
            self.x += 5

    def move_up(self):
        if self.y >0:
            self.y -= 5

    def move_down(self):
        if self.y < WINDOW_HEIGHT-78:
            self.y += 5

    def fire(self):
        # 发射子弹
        # 创建子弹对象 子弹x = 飞机x +飞机宽度的一半-字段宽度的一半
        bullet = HeroBullet("res/bullet_9.png", self.x + 60 - 10, self.y - 31, self.window)
        bullet.display()
        self.bullets.append(bullet)

    def display_bullets(self):

        # 超出界面需要删除的子弹
        delete_bullets = []

        for bullet in self.bullets:
            if bullet.y > -31:
                bullet.display()
                bullet.move()
            else:  # 飞出边界
                delete_bullets.append(bullet)
            for enemy in enemy_list:
                if bullet.is_hit_enemy(enemy):
                    enemy.is_hited = True
                    delete_bullets.append(bullet)
                    global score
                    score += 10
                    break
        # 删除飞出边界的子弹
        for out_window_bullet in delete_bullets:
            self.bullets.remove(out_window_bullet)

    def is_hit_enemy(self,enemy):
        # 判断是否碰撞敌机
        if pygame.Rect.colliderect(
            pygame.Rect(self.x,self.y,100,68),
            pygame.Rect(enemy.x,enemy.y,80,58)
        ):
            return True
        else:
            return False

    def display(self):
        for enemy in enemy_list:
            if self.is_hit_enemy(enemy):
                enemy.is_hited = True
                time.sleep(3)
                sys.exit()
                pygame.quit()
                break

        self.window.blit(self.img,(self.x,self.y))

class EnemyPlane(BasePlane):
    """创建敌机对象"""

    def __init__(self, image_path, x, y, window):
        super().__init__(image_path, x, y, window)
        self.is_hited = False

    def display(self):
        if self.is_hited:
            self.x = random.randint(0, WINDOW_HEIGHT - 100)
            self.y = 0
            self.is_hited = False
        self.window.blit(self.img, (self.x, self.y))

    def move(self):
        self.y += 10
        # 如果到达下边界，回到顶部
        if self.y >= WINDOW_HEIGHT:
            self.x = random.randint(0, random.randint(0, 512 - 100))
            self.y = 0


class Game(object):
    def __init__(self):
        pygame.init()  # 初始化pygame库，让计算机做好准备
        # 设置标题
        pygame.display.set_caption("飞机大战 v1.14")

        # 设置图标
        pygame_ico = pygame.image.load("res/app.ico")
        pygame.display.set_icon(pygame_ico)
        pygame.mixer.music.load("res/bg2.ogg")

        self.gameover_sound =  pygame.mixer.Sound("res/gameover.wav")
        pygame.mixer.music.play(-1)

        self.window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

        self.game_map = Map("res/img_bg_level_%d.jpg" % random.randint(1,5),self.window)

        self.hero_plane = HeroPlane("res/hero2.png", 240, 500, self.window)
        enemy_plane1 = EnemyPlane("res/img-plane_5.png", random.randint(0, 512 - 100), 0, self.window)
        enemy_plane2 = EnemyPlane("res/img-plane_3.png", random.randint(0, 512 - 100), random.randint(-400, -150),
                                  self.window)
        enemy_plane3 = EnemyPlane("res/img-plane_4.png", random.randint(0, 512 - 100), random.randint(-600, -400),
                                  self.window)
        enemy_list.append(enemy_plane1)
        enemy_list.append(enemy_plane2)
        enemy_list.append(enemy_plane3)

        self.enemy_list = enemy_list

        self.score_font = pygame.font.SysFont("res/SIMHEI.TTF",40)

    def draw_text(self,content,size,x,y):
        font_obj = pygame.font.Font("res/SIMHEI.TTF",size)
        text = font_obj.render(content,1,(255,255,255))
        self.window.blit(text,(x,y))

    def wait_game_input(self):
        while True:
            for event in pygame.event.get():
                if event.type ==  QUIT:
                    sys.exit()
                    pygame.quit()
                elif event.type == KEYDOWN:

                    if event.key == K_ESCAPE:
                        sys.exit()
                        pygame.quit()
                    elif event.key == K_RETURN:
                        global is_restart,score
                        is_restart = True
                        score = 0
                        return

    def game_start(self):
        self.game_map.display()
        self.draw_text("飞机大战",40,WINDOW_WIDTH/2 - 100,WINDOW_HEIGHT / 3)
        self.draw_text("按下enter开始游戏，Esc退出游戏。",28,WINDOW_WIDTH / 3 - 140, WINDOW_HEIGHT / 2)
        pygame.display.update()
        self.wait_game_input()

    def game_over(self):
        pygame.mixer.music.stop()
        self.gameover_sound.play()
        self.game_map.display()
        self.draw_text("战机被击落，得分为%d " % score,28,WINDOW_WIDTH / 3 - 140, WINDOW_HEIGHT / 2)
        self.draw_text("按下enter开始游戏，Esc退出游戏。", 28, WINDOW_WIDTH / 3 - 140, WINDOW_HEIGHT / 2)
        pygame.display.update()
        self.wait_game_input()
        self.gameover_sound.stop()

    def run(self):
        if is_restart == False:
            self.game_start()

        while True:
            print("121111")
            self.game_map.display()
            self.game_map.move()
            self.hero_plane.display()

            if self.hero_plane.is_hited:
                self.hero_plane.is_hited = False
                global enemy_list
                enemy_list = []
                break

            self.hero_plane.display_bullets()

            for enemy in enemy_list:
                enemy.display()
                enemy.move()

            score_text = self.score_font.render("得分:%d " % score, 1, (255,255,255))
            self.window.blit(score_text,(10,10))

            pygame.display.update()

            for event in pygame.event.get():

                if event.type == QUIT:
                    # 让程序终止
                    sys.exit()
                    pygame.quit()

                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.hero_plane.fire()

            # 获取连续按下的情况
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_LEFT]:
                self.hero_plane.move_left()

            if pressed_keys[pygame.K_RIGHT]:
                self.hero_plane.move_right()

            if pressed_keys[pygame.K_DOWN]:
                self.hero_plane.move_down()

            if pressed_keys[pygame.K_UP]:
                self.hero_plane.move_up()

            # 使程序休眠，释放内存
            time.sleep(0.01)

        self.game_over()


def main():
    while True:
        game = Game()
        game.run()

if __name__ == "__main__":
    main()
