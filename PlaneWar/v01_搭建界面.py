"""
   main 函数：主程序，写项目中的主要流程代码【逻辑代码】
"""
import pygame

# 定义常量
WINDOW_HEIGHT = 768
WINDOW_WIDTH = 512


#定义主程序

def main():
    """主逻辑函数"""
    pygame.init()  #初始化pygame库，让计算机做好准备

    """1.创建窗口"""
    window=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    """2.贴背景图片"""
    bg_img=pygame.image.load("res/img_bg_level_1.jpg")

    while True:
        # 贴图，把图片贴到窗口中， blit(图像对象，相对原点的坐标)
        window.blit(bg_img,(0,0))
        # 刷新界面，不刷新不会更新显示内容
        pygame.display.update()


if __name__=="__main__":
    main()

