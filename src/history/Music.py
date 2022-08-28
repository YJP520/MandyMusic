#
# MandyMusic 2022 by Pycharm.
# Time : 2022/08/26
# Author : YU.J.P
#

"""
    V1.0.0
    新增功能：
       1. 音乐播放基本功能

"""
import time  # 时间包
import random  # 随机包
import pygame  # 游戏引擎安装成功

# 全局变量
VERSION = 'MandyMusic V1.0.0'
DEFAULT_HEIGHT = 16 * 30  # 默认窗口高度
DEFAULT_WIDTH = 16 * 50  # 默认窗口宽度
COLOR_BACKGROND = pygame.Color(202, 231, 255)  # 背景颜色 RGB合成颜色 (156, 191, 238) (221, 227, 247) (202, 231, 255)
FONT = '方正粗黑宋简体'
COLOR_FONT = pygame.Color(24, 72, 172)  # 字体颜色 RGB合成颜色 24, 72, 172
SIZE_FONT = 24  # 字体大小
GETTEXT_X = 5  # 提示文字 x 坐标
GETTEXT_Y = 5  # 提示文字 y 坐标
SCORE_X = 5  # 得分文字 x 坐标
SCORE_Y = 100  # 得分文字 y 坐标
DELAY = 0.01  # 循环延时时间

# 音乐播放类
class Music():
    def __init__(self, fileName):
        self.fileName = fileName
        # 先初始化音乐混响器
        pygame.mixer.init()
        pygame.mixer.music.load(self.fileName)

    # 开始播放音效
    def startPlay(self):
        pygame.mixer.music.play(loops=0)  # 单独播放一次

    # 暂停播放音乐
    def stopPlayTemp(self):
        pass

    # 停止播放音乐
    def stopPlay(self):
        pygame.mixer.music.stop()


# 主播放类
class MainMusic():
    window = None  # 播放器主窗口
    SCREEN_HEIGHT = DEFAULT_HEIGHT  # 窗口高度
    SCREEN_WIDTH = DEFAULT_WIDTH  # 窗口宽度

    musicName = ' '  # 正在播放音乐名字
    isPlay = True  # 播放标志
    music = None  # 创建音乐对象

    def __init__(self):
        pass

    # 开始游戏
    def startGame(self):
        pygame.display.init()  # 窗口初始化
        # 创建窗口加载窗口(借鉴官方文档)
        MainMusic.window = pygame.display.set_mode([MainMusic.SCREEN_WIDTH, MainMusic.SCREEN_HEIGHT])
        # 设置游戏标题
        pygame.display.set_caption(VERSION)
        # 默认音乐
        MainMusic.music = Music('musics/' + MainMusic.musicName)
        # 让窗口持续刷新操作
        while True:
            # 给窗口一个填充色
            MainMusic.window.fill(COLOR_BACKGROND)
            # 在循坏中持续完成事件的获取
            self.getEvent()
            # 赛况信息 将绘制文字得到的小画布，放到窗口上
            MainMusic.window.blit(self.getTextSurface("本地音乐: %d" \
                % 1000, FONT, SIZE_FONT, COLOR_FONT), (GETTEXT_X, GETTEXT_Y))
            # 得分信息 将绘制文字得到的小画布，放到窗口上
            MainMusic.window.blit(self.getTextSurface("正在播放: %s" \
                % MainMusic.musicName, FONT, SIZE_FONT, COLOR_FONT), (SCORE_X, SCORE_Y))
            #暴力延时
            time.sleep(DELAY)  # 延时 DELAYs
            # 窗口的刷新
            pygame.display.update()

    # 左上角文字绘制的功能
    def getTextSurface(self, text, font, size, color):
        # 字体初始化模块
        pygame.font.init()
        # 选中一个合适的字体
        # fontList = pygame.font.get_fonts()  # 获取目前所有字体
        # for font in fontList:
        #     print(font)
        theFont = pygame.font.SysFont(font, size)
        # 使用对应的字体完成相关内容的绘制
        textSurface = theFont.render(text, True, color)
        return textSurface

    # 获取程序运行期间所有事件（鼠标事件，键盘事件）
    def getEvent(self):
        # 1.获取所有事件
        eventList = pygame.event.get()
        # 2.对事件进行判断处理（1.点击关闭按钮，2.按下键盘的某个按键）
        for event in eventList:
            # 判断event.type 是否QUIT，如果是退出的话，直接调用程序结束方法
            if event.type == pygame.QUIT:
                self.endGame()
            # 判断事件类型是否为按键按下，如果是，继续判断按键是哪一个按键，进行对应处理
            if event.type == pygame.KEYDOWN:
                if True:
                    # 判断具体是哪一个按键的处理
                    if event.key == pygame.K_LEFT:  # 左方向键
                        print('坦克向左调头，移动')
                    elif event.key == pygame.K_RIGHT:  # 右方向键
                        print('坦克向右调头，移动')
                    elif event.key == pygame.K_UP:  # 上方向键
                        print('坦克向上调头，移动')
                    elif event.key == pygame.K_DOWN:  # 下方向键
                        print('坦克向下调头，移动')
                    elif event.key == pygame.K_SPACE:  # 空格键控制音乐播放
                        if MainMusic.isPlay:
                            print('音乐播放')
                            # 调用音乐播放方法
                            MainMusic.music.startPlay()
                            # 改变播放状态
                            MainMusic.isPlay = False
                        else:
                            print('音乐暂停')
                            # 调用音乐停止播放方法
                            MainMusic.music.stopPlay()
                            # 改变播放状态
                            MainMusic.isPlay = True
                elif event.key == pygame.K_ESCAPE:  # ESC键重生
                    pass
            if event.type == pygame.KEYUP:
                if True:
                    # 松开的是方向键，才更改移动状态
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT \
                        or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        pass

    # 游戏胜利
    def isSucceed(self):
        # 游戏结束
        MainMusic.window.blit(self.getTextSurface("SUCCEED ！", 'kaiti', 64, COLOR_FONT), (128 * 2, 128 * 1))

    # 结束游戏
    def endGame(self):
        print('谢谢使用！')
        exit()  # 结束python解释器


if __name__ == '__main__':
    MainMusic().startGame()  # 开始游戏
