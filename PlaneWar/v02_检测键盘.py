"""
   main 函数：主程序，写项目中的主要流程代码【逻辑代码】
"""
# 导入动态模块(.dll .pyd .so)
import pygame

from pygame.locals import *
import sys

# 定义常量
WINDOW_HEIGHT = 768
WINDOW_WIDTH = 512


#定义主程序

def main():
    """主逻辑函数"""
    pygame.init()  # 初始化pygame库，让计算机做好准备

    """1.创建窗口"""
    # 并设置窗口尺寸
    window=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    """2.贴背景图片"""
    bg_img=pygame.image.load("res/img_bg_level_1.jpg")

    while True:
        # 贴图，把图片贴到窗口中， blit(图像对象，相对原点的坐标)
        window.blit(bg_img,(0,0))
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
                    print("space")
                elif event.key == K_LEFT:
                    print("left")
                elif event.key == K_RIGHT:
                    print("right")





if __name__=="__main__":
    main()

