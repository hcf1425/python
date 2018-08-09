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


# 定义飞机基类
class BasePlane(object):

    def __init__(self, img_path, x, y, window):
        self.img = pygame.image.load(img_path)
        self.x = x
        self.y = y
        self.window = window

    def display(self):
        self.window.blit(self.img,(self.x,self.y))


# 定义英雄飞机类
class HeroPlane(BasePlane):

    def __init__(self, image_path, x, y, window):
        super().__init__(image_path, x, y, window)
        self.bullets = []

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def fire(self):
        # 发射子弹
        # 创建子弹对象 子弹x = 飞机x +飞机宽度的一半-字段宽度的一半
        bullet = HeroBullet("res/bullet_9.png",self.x+60-10,self.y-31,self.window)
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

        # 删除飞出边界的子弹
        for out_window_bullet in delete_bullets:
            self.bullets.remove(out_window_bullet)


class EnemyPlane(BasePlane):
    """创建敌机对象"""

    def move(self):
        self.y +=10
        # 如果到达下边界，回到顶部
        if self.y >=WINDOW_HEIGHT:
            self.x = random.randint(0,random.randint(0,512-100))
            self.y = 0

# 定义主程序
def main():
    """主逻辑函数"""
    pygame.init()  # 初始化pygame库，让计算机做好准备

    """1.创建窗口"""
    # 并设置窗口尺寸
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    """2.贴背景图片"""
    bg_img = pygame.image.load("res/img_bg_level_1.jpg")
    """3.贴飞机图片"""
    # hero_plane_img = pygame.image.load("res/hero2.png")
    # x = 240
    # y = 500

    # 创建飞机对象
    hero_plane = HeroPlane("res/hero2.png",240,500,window)
    enemy_plane = EnemyPlane("res/img-plane_5.png",random.randint(0,512-100),0,window)

    while True:
        # 贴背景图，把图片贴到窗口中， blit(图像对象，相对原点的坐标)
        window.blit(bg_img, (0, 0))

        # 贴飞机图
        # window.blit(hero_plane_img,(x,y))

        hero_plane.display()
        hero_plane.display_bullets()

        enemy_plane.display()
        enemy_plane.move()

        # 刷新界面，不刷新不会更新显示内容
        pygame.display.update()

        # 获取事件，如按键等，先显示界面，再根据获取的事件，修改界面效果

        for event in pygame.event.get():

            if event.type == QUIT:
                # 让程序终止
                sys.exit()
                pygame.quit()

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    hero_plane.fire()

        # 获取连续按下的情况
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            hero_plane.move_left()

        if pressed_keys[pygame.K_RIGHT]:
            hero_plane.move_right()

        # 使程序休眠，释放内存
        time.sleep(0.01)


if __name__ == "__main__":
    main()
