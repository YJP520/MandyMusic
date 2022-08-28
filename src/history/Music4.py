#
# MandyMusic 2022 by Pycharm.
# Time : 2022/08/28
# Author : YU.J.P
#

"""
    版本: V1.0.3
    基本功能:
        1.音乐音量 增减 控制；
        2.音乐 暂停/继续 播放；
        3.音乐切换 上一首/下一首；
        4.修改应用图标 - FMJJ.jpg；
        5.显示音乐歌曲名信息；
        6.显示播放时间与单曲时长；
        7.自动循环播放；
        8.音乐切换 上一首/下一首 图形组件；
        9.播放时间与单曲时长 格式化；
        10.图形化点击播放按钮；
        11.播放列表设置；
        12.自动播放的三种模式 列表循环 单曲循环 随机播放；
        13.播放 上一曲/下一曲 可以有 随机/列表 播放；
        14.播放模式图形加载 鼠标点击；
    更新内容 :
        - 优化鼠标点击 鼠标点击抖动的问题；
        - 鼠标在特定按钮上会让光标改变样式；
        - 新增图形组件 播放列表 音量 设置；
        - 背景图片 简洁清新；
        - 播放进度条显示；
        - 进度条的拖动 播放时间自动切换；
    需求：
        - 完善新的歌曲类 即每首歌曲需要专门管理 歌曲所有相关 便于管理和展示；
        - 简单显示歌词 - 自定义；
        -

"""
import copy  # 拷贝函数
import os  # 文件输入
import random  # 随机包
import tkinter  # 窗口视窗
import threading  # 多线程操作
import pygame  # 游戏引擎
from mutagen.mp3 import MP3  # 获取mp3总时长

# 全局变量
VERSION = 'MandyMusic V1.0.3'
DEFAULT_HEIGHT = 16 * 30  # 默认窗口高度
DEFAULT_WIDTH = 16 * 50  # 默认窗口宽度
COLOR_BACKGROUND = pygame.Color(3, 25, 62)  # 背景颜色 RGB合成颜色 (156, 191, 238) (221, 227, 247) (202, 231, 255)
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load('images/Player_Wallpaper.png'), (800, 480))  # 合适大小
Singer_IMAGE = pygame.image.load('images/封茗囧菌.png')  # 样例图片
THEME_FONT = 'dengxian'  # 主题字体 默认等线
COLOR_FONT = pygame.Color(255, 255, 255)  # 字体颜色 RGB合成颜色 (24, 72, 172) (255, 255, 255)
PLAY_FONT = 'dengxian'  # 播放显示字体

SIZE_FONT = 24  # 主题字体大小
TIME_SIZE_FONT = 24  # 时间显示字体大小
PLAY_SIZE_FONT = 32  # 播放信息显示字体大小

GETTEXT_X, GETTEXT_Y = 5, 5  # 提示文字 x y 坐标
PLAY_INFO_X, PLAY_INFO_Y = 16 * 14, 16 * 4 # 播放信息显示 x y 坐标
VOLUME_X, VOLUME_Y = 16 * 40, 5  # 音量文字 x y 坐标
TIME_X, TIME_Y = 16 * 9, 16 * 24 - 4  # 播放时间显示 x y 坐标
PLAY_STOP_X, PLAY_STOP_Y = 16 * 24, 16 * 26  # 播放暂停组件 x y 坐标
LAST_X, LAST_Y = 16 * 20, 16 * 26  # 上一曲组件 x y 坐标
NEXT_X, NEXT_Y = 16 * 28, 16 * 26  # 下一曲组件 x y 坐标
PLAY_PATTERN_X, PLAY_PATTERN_Y = 16 * 16, 16 * 26  # 播放模式组件 x y 坐标
PLAYLIST_X, PLAYLIST_Y = 16 * 32, 16 * 26  # 播放列表组件 x y 坐标
PLAYSOUND_X, PLAYSOUND_Y = 16 * 36, 16 * 26  # 播放音量组件 x y 坐标
PLAY_SETTING_X, PLAY_SETTING_Y = 16 * 12, 16 * 26  # 播放设置组件 x y 坐标
PROGRESS_BAR_X, PROGRESS_BAR_Y = 200, 16 * 24 # 播放进度条显示 x y 坐标

FILENAME = 'musics'  # 音乐存储文件夹
DELAY = 0.01  # 循环延时时间


# 音乐播放类
class Music:
    def __init__(self, fileName):
        self.fileName = fileName
        # 先初始化音乐混响器
        pygame.mixer.init()
        pygame.mixer.music.load(self.fileName)
        self.setVolume()  # 设置音量

    # 开始播放音效
    def startPlay(self):
        # 获取音乐的时长
        if MainMusic.playPattern == 2:
            MainMusic.musicTime = MP3(MainMusic.shuffle_List[MainMusic.musicNumber]).info.length
        else:
            MainMusic.musicTime = MP3(MainMusic.Musics_List[MainMusic.musicNumber]).info.length
        # 时长信息设置
        MainMusic.musicTimeInfo.getStringOfTime(MainMusic.musicTime)
        # 改变播放状态
        MainMusic.isPlay = False
        # 更改进度条调节标志
        MainMusic.isUpdateTime = False
        # 播放音乐
        pygame.mixer.music.play(loops=0)  # 单独播放一次

    # 暂停播放音乐
    def playPause(self):
        pygame.mixer.music.pause()  # 音乐暂停播放语句

    # 继续播放语句
    def playUnPause(self):
        pygame.mixer.music.unpause()  # 音乐继续播放语句

    # 停止播放音乐
    def stopPlay(self):
        pygame.mixer.music.stop()

    # 设置音乐音量
    def setVolume(self):
        pygame.mixer.music.set_volume(float(MainMusic.VolumeValue) / 100)

    # 音量加 1
    def addVolume(self):
        if MainMusic.VolumeValue < 100:
            MainMusic.VolumeValue += 1
            self.setVolume()
            print('音量:%d' % MainMusic.VolumeValue)
        else:
            print('最大音量...')

    # 音量减 1
    def subVolume(self):
        if MainMusic.VolumeValue > 0:
            MainMusic.VolumeValue -= 1
            self.setVolume()
            print('音量:%d' % MainMusic.VolumeValue)
        else:
            print('最小音量...')


# 时间显示组件
class TimeOfMusic:
    def __init__(self):
        self.minutes = 0  # 分钟
        self.seconds = 0  # 秒钟
        self.timeString = None  # 固定属性

    # 根据总时间设置时间
    def setTime(self, seconds):
        # 获取分钟数
        self.minutes = int(seconds) // 60
        # 获取秒钟数
        self.seconds = int(seconds) % 60

    # 显示时间字符串
    def getStringOfTime(self, seconds):
        # 根据总时间设置时间
        self.setTime(seconds)
        # 初始格式
        self.timeString = None
        # 时钟设置
        if 0 <= self.minutes < 10:
            self.timeString = '0' + str(self.minutes)
        else:
            self.timeString = str(int(self.minutes))
        # 加分隔符
        self.timeString += ':'
        # 秒钟设置
        if 0 <= self.seconds < 10:
            self.timeString += '0' + str(int(self.seconds))
        else:
            self.timeString += str(self.seconds)
        # 返回字符串
        return self.timeString


# 播放暂停 组件
class PlayAndStop():
    def __init__(self, left, top):
        # 图片集
        self.images = {
            False: pygame.image.load('components/mini/Player_Play_mini.gif'),
            True: pygame.image.load('components/mini/Player_Stop_mini.gif')
        }
        self.image = self.images[False]
        # 组件所在的区域 rect
        self.rect = self.image.get_rect()
        # 指定组件初始化位置,分别是x,y轴的位置
        self.rect.left = left
        self.rect.top = top

    # 组件展示
    def displayPlayAndStop(self):
        # 1.重新设置组件的图片
        self.image = self.images[MainMusic.isPlay]
        # 2.将组件加入到窗口中
        MainMusic.window.blit(self.image, self.rect)


# 上一曲 / 下一曲 组件
class LastAndNext:
    def __init__(self, left, top, lastOrNext):
        # 图片集
        self.images = {
            False: pygame.image.load('components/mini/Player_Last_mini.gif'),
            True: pygame.image.load('components/mini/Player_Next_mini.gif')
        }
        self.image = self.images[lastOrNext]
        # 组件所在的区域 rect
        self.rect = self.image.get_rect()
        # 指定组件初始化位置,分别是x,y轴的位置
        self.rect.left = left
        self.rect.top = top

    # 组件展示
    def displayLastAndNext(self):
        # 将组件加入到窗口中
        MainMusic.window.blit(self.image, self.rect)


# 播放模式小组件
class PlayPattern:
    def __init__(self, left, top, Pattern):
        # 图片集
        self.images = {
            0: pygame.image.load('components/mini/Player_Order_mini.gif'),
            1: pygame.image.load('components/mini/Player_Loop_mini.gif'),
            2: pygame.image.load('components/mini/Player_Random_mini.gif')
        }
        self.image = self.images[Pattern]
        # 组件所在的区域 rect
        self.rect = self.image.get_rect()
        # 指定组件初始化位置,分别是x,y轴的位置
        self.rect.left = left
        self.rect.top = top

    # 组件展示
    def displayPlayPattern(self):
        # 1.重新设置组件的图片
        self.image = self.images[MainMusic.newPattern]
        # 2.将组件加入到窗口中
        MainMusic.window.blit(self.image, self.rect)


# 播放列表小组件
class PlayList:
    def __init__(self, left, top):
        # 单图
        self.image = pygame.image.load('components/mini/Player_List_mini.gif')
        # 组件所在的区域 rect
        self.rect = self.image.get_rect()
        # 指定组件初始化位置,分别是x,y轴的位置
        self.rect.left = left
        self.rect.top = top

    # 组件展示
    def displayPlayList(self):
        # 将组件加入到窗口中
        MainMusic.window.blit(self.image, self.rect)


# 播放音量小组件
class PlaySound:
    def __init__(self, left, top):
        # 单图
        self.image = pygame.image.load('components/mini/Player_Sound_mini.gif')
        # 组件所在的区域 rect
        self.rect = self.image.get_rect()
        # 指定组件初始化位置,分别是x,y轴的位置
        self.rect.left = left
        self.rect.top = top

    # 组件展示
    def displayPlaySound(self):
        # 将组件加入到窗口中
        MainMusic.window.blit(self.image, self.rect)


# 播放设置小组件
class PlaySetting:
    def __init__(self, left, top):
        # 单图
        self.image = pygame.image.load('components/mini/Player_Setting_mini.gif')
        # 组件所在的区域 rect
        self.rect = self.image.get_rect()
        # 指定组件初始化位置,分别是x,y轴的位置
        self.rect.left = left
        self.rect.top = top

    # 组件展示
    def displayPlaySetting(self):
        # 将组件加入到窗口中
        MainMusic.window.blit(self.image, self.rect)


# 播放进度条小组件
class ProgressBar:
    def __init__(self, left, top):
        # 单图
        self.image = pygame.image.load('components/mini/Player_ProgressBar_mini.gif')
        # 组件所在的区域 rect
        self.rect = self.image.get_rect()
        # 指定组件初始化位置,分别是x,y轴的位置
        self.rect.left = left
        self.rect.top = top

    # 组件展示
    def displayProgressBar(self):
        # 将组件加入到窗口中
        MainMusic.window.blit(self.image, self.rect)

# 播放进度条指示点小组件
class ProgressBoll:
    def __init__(self, left, top):
        # 单图
        self.image = pygame.image.load('components/mini/Player_ProgressBoll_mini.gif')
        # 组件所在的区域 rect
        self.rect = self.image.get_rect()
        # 指定组件初始化位置,分别是x,y轴的位置
        self.rect.left = left
        self.rect.top = top


    # 更新指示点位置
    def setLeft(self):
        # 导入常量
        global PROGRESS_BAR_X
        # 播放完归位
        if MainMusic.isOver:
            self.rect.left = PROGRESS_BAR_X
        else:
            # 根据时间进度加载位置
            percentage = MainMusic.playTime / MainMusic.musicTime
            self.rect.left = PROGRESS_BAR_X + int(384 * percentage)

            # 组件展示
    def displayProgressBoll(self):
        # 1.更新坐标
        self.setLeft()
        # 2.将组件加入到窗口中
        MainMusic.window.blit(self.image, self.rect)


# 主播放类
class MainMusic():
    window = None  # 播放器主窗口
    SCREEN_HEIGHT = DEFAULT_HEIGHT  # 窗口高度
    SCREEN_WIDTH = DEFAULT_WIDTH  # 窗口宽度

    musicNumber = 0  # 默认第一首
    musicName = ''  # 歌曲名
    Musics_List = None  # 默认顺序音乐列表
    shuffle_List = None  # 随机列表
    playPattern = 0  # 自动播放模式 0：列表循环，1：单曲循环，2：随机播放
    newPattern = 0  # 新的播放模式 解决切换模式改列表的问题
    isPlay = True  # 播放标志-暂停/继续
    isOver = False  # 单曲是否播放完成
    music = None  # 创建音乐对象
    musicTime = 0  # 歌曲播放时间
    musicTimeInfo = TimeOfMusic()  # 时间字符串对象
    playTime = 0  # 已经播放时长
    startPos = 0  # 更新的播放时长
    isUpdateTime = False  # 是否更新播放位置
    playTimeInfo = TimeOfMusic()  # 时间字符串对象

    VolumeValue = 10  # 音量范围 0-100，音量初始值为 10

    thePlayAndStop = None  # 播放/暂停 组件
    theLast = None  # 上一曲 组件
    theNext = None  # 下一曲 组件
    thePattern = None  # 播放模式组件
    thePlayList = None  # 播放列表组件
    thePlaySound = None  # 播放音量组件
    thePlaySetting = None  # 播放设置组件
    theProgressBar = None  # 进度条组件
    theProgressBoll = None  # 进度条指示点组件

    def __init__(self):
        pass

    # 从文件夹中导入文件的方法
    def musicFromFile(self, fileName):
        # 定义 Musics 列表
        Musics = []
        # 遍历 musics 文件夹
        for root, dirs, files in os.walk(fileName):
            for file in files:
                # 找出所有的.mp3文件
                if os.path.splitext(file)[1] == '.mp3':
                    # 把所有.mp3文件写入 Musics 数组
                    Musics.append(os.path.join(root, file))
        # 返回 Musics 数组
        return Musics

    # 创建组件
    def createComponent(self):
        # 播放暂停组件
        MainMusic.thePlayAndStop = PlayAndStop(PLAY_STOP_X, PLAY_STOP_Y)
        # 加载上一曲/下一曲组件
        MainMusic.theLast = LastAndNext(LAST_X, LAST_Y, False)  # 上一曲
        MainMusic.theNext = LastAndNext(NEXT_X, NEXT_Y, True)  # 下一曲
        # 加载播放模式组件
        MainMusic.thePattern = PlayPattern(PLAY_PATTERN_X, PLAY_PATTERN_Y, MainMusic.playPattern)
        # 加载播放列表组件
        MainMusic.thePlayList = PlayList(PLAYLIST_X, PLAYLIST_Y)
        # 加载播放音量组件
        MainMusic.thePlaySound = PlaySound(PLAYSOUND_X, PLAYSOUND_Y)
        # 加载设置组件
        MainMusic.thePlaySetting = PlaySetting(PLAY_SETTING_X, PLAY_SETTING_Y)
        # 加载进度条组件
        MainMusic.theProgressBar = ProgressBar(PROGRESS_BAR_X, PROGRESS_BAR_Y)
        # 加载进度指示点组件
        MainMusic.theProgressBoll = ProgressBoll(PROGRESS_BAR_X, PROGRESS_BAR_Y)

    # 将组件加载到窗口中
    def blitComponent(self):
        MainMusic.thePlayAndStop.displayPlayAndStop()
        MainMusic.theLast.displayLastAndNext()
        MainMusic.theNext.displayLastAndNext()
        MainMusic.thePattern.displayPlayPattern()
        MainMusic.thePlayList.displayPlayList()
        MainMusic.thePlaySound.displayPlaySound()
        MainMusic.thePlaySetting.displayPlaySetting()
        MainMusic.theProgressBar.displayProgressBar()
        MainMusic.theProgressBoll.displayProgressBoll()

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

    # 音乐播放/暂停 切换
    def playOrStop(self):
        if MainMusic.isPlay:
            print('音乐播放')
            # 调用音乐继续播放方法
            MainMusic.music.playUnPause()
            # 改变播放状态
            MainMusic.isPlay = False
        else:
            print('音乐暂停')
            # 调用音乐暂停播放方法
            MainMusic.music.playPause()
            # 改变播放状态
            MainMusic.isPlay = True

    # 上一曲 默认循环播放
    def playLastMusic(self):
        # 获取当前播放模式
        MainMusic.playPattern = MainMusic.newPattern
        # 列表顺序加载
        if MainMusic.musicNumber > 0:
            MainMusic.musicNumber -= 1
        elif MainMusic.musicNumber <= 0:
            MainMusic.musicNumber = len(MainMusic.Musics_List) - 1
        # 重新加载音乐
        # 重新加载音乐 列表不同实现随机
        if MainMusic.playPattern == 2:  # 随机列表循环 实现随机播放
            MainMusic.music = Music(MainMusic.shuffle_List[MainMusic.musicNumber])
        else:  # 默认列表循环
            MainMusic.music = Music(MainMusic.Musics_List[MainMusic.musicNumber])
        # 播放音乐
        MainMusic.music.startPlay()

    # 下一曲 默认循环播放
    def playNextMusic(self):
        # 获取当前播放模式
        MainMusic.playPattern = MainMusic.newPattern
        # 列表顺序加载
        if MainMusic.musicNumber < len(MainMusic.Musics_List) - 1:
            MainMusic.musicNumber += 1
        elif MainMusic.musicNumber >= len(MainMusic.Musics_List) - 1:
            MainMusic.musicNumber = 0
        # 重新加载音乐 列表不同实现随机
        if MainMusic.playPattern == 2:  # 随机列表循环 实现随机播放
            MainMusic.music = Music(MainMusic.shuffle_List[MainMusic.musicNumber])
        else:  # 默认列表循环
            MainMusic.music = Music(MainMusic.Musics_List[MainMusic.musicNumber])
        # 播放音乐
        MainMusic.music.startPlay()

    # 单曲循环
    def playThisMusic(self):
        # 重新加载同一首音乐
        MainMusic.music = Music(MainMusic.Musics_List[MainMusic.musicNumber])
        # 播放音乐
        MainMusic.music.startPlay()

    # 播放模式切换
    def switchPattern(self):
        # 进来一次 模式切换 +1
        MainMusic.newPattern += 1
        # 模式自动归位
        if MainMusic.newPattern > 2:
            MainMusic.newPattern = 0

    # 自动切换下一首 列表循环播放 pattern播放模式
    def autoPlay(self):
        if MainMusic.playTime >= MainMusic.musicTime - 0.1:
            MainMusic.isOver = True
        if MainMusic.isOver:
            # 获取当前播放模式
            MainMusic.playPattern = MainMusic.newPattern
            # 根据播放模式播放音乐
            if MainMusic.playPattern == 0:  # 列表循环播放
                # 默认列表 加载下一曲
                self.playNextMusic()
            elif MainMusic.playPattern == 1:  # 单曲循环播放
                # 加载本曲
                self.playThisMusic()
            elif MainMusic.playPattern == 2:  # 随机单曲播放
                # 随机列表 加载下一曲
                self.playNextMusic()
            # 播放音乐
            MainMusic.music.startPlay()
            # 更改判断标志
            MainMusic.isOver = False

    # 获取程序运行期间所有事件（鼠标事件，键盘事件）
    def getEvent(self):
        # 1.获取所有事件
        eventList = pygame.event.get()
        # 2.对事件进行判断处理（1.点击关闭按钮，2.按下键盘的某个按键）
        for event in eventList:
            # 判断event.type 是否QUIT，如果是退出的话，直接调用程序结束方法
            if event.type == pygame.QUIT:
                self.endUse()

            # 2.1 鼠标事件
            # 获取鼠标坐标
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # 根据位置改变改光标 判断是否鼠标的坐标在按钮的坐标范围内
            if PLAY_STOP_X <= mouse_x <= PLAY_STOP_X + MainMusic.thePlayAndStop.rect.width and \
                PLAY_STOP_Y <= mouse_y <= PLAY_STOP_Y + MainMusic.thePlayAndStop.rect.height or \
                LAST_X <= mouse_x <= LAST_X + MainMusic.theLast.rect.width and \
                LAST_Y <= mouse_y <= LAST_Y + MainMusic.theLast.rect.height or \
                NEXT_X <= mouse_x <= NEXT_X + MainMusic.theNext.rect.width and \
                NEXT_Y <= mouse_y <= NEXT_Y + MainMusic.theNext.rect.height or \
                PLAY_PATTERN_X <= mouse_x <= PLAY_PATTERN_X + MainMusic.thePattern.rect.width and \
                PLAY_PATTERN_Y <= mouse_y <= PLAY_PATTERN_Y + MainMusic.thePattern.rect.height or \
                PLAYLIST_X <= mouse_x <= PLAYLIST_X + MainMusic.thePlayList.rect.width and \
                PLAYLIST_Y <= mouse_y <= PLAYLIST_Y + MainMusic.thePlayList.rect.height or \
                PLAY_SETTING_X <= mouse_x <= PLAY_SETTING_X + MainMusic.thePlaySetting.rect.width and \
                PLAY_SETTING_Y <= mouse_y <= PLAY_SETTING_Y + MainMusic.thePlaySetting.rect.height or \
                PLAYSOUND_X <= mouse_x <= PLAYSOUND_X + MainMusic.thePlaySound.rect.width and \
                PLAYSOUND_Y <= mouse_y <= PLAYSOUND_Y + MainMusic.thePlaySound.rect.height:
                # 特殊光标
                pygame.mouse.set_cursor(pygame.cursors.diamond)
            # 进度条 特殊光标
            elif PROGRESS_BAR_X <= mouse_x <= PROGRESS_BAR_X + MainMusic.theProgressBar.rect.width and \
                PROGRESS_BAR_Y <= mouse_y <= PROGRESS_BAR_Y + MainMusic.theProgressBar.rect.height:
                # 特殊光标
                pygame.mouse.set_cursor(pygame.cursors.broken_x)
            else:
                # 原始光标
                pygame.mouse.set_cursor(pygame.cursors.arrow)

            # 鼠标抬起事件
            if event.type == pygame.MOUSEBUTTONUP:
                # 如果为左键:1,滑轮:2,右键:3
                if  event.button == 1:
                    # 判断是否点击了暂停或播放 - 判断是否鼠标的坐标在暂停播放按钮的坐标范围内
                    if PLAY_STOP_X <= mouse_x <= PLAY_STOP_X + MainMusic.thePlayAndStop.rect.width and \
                            PLAY_STOP_Y <= mouse_y <= PLAY_STOP_Y + MainMusic.thePlayAndStop.rect.height:
                        # 音乐播放/暂停 切换
                        MainMusic.playOrStop(self)
                    # 判断是否点击了上一曲 - 判断是否鼠标的坐标在暂停播放按钮的坐标范围内
                    elif LAST_X <= mouse_x <= LAST_X + MainMusic.theLast.rect.width and \
                        LAST_Y <= mouse_y <= LAST_Y + MainMusic.theLast.rect.height:
                        # 播放上一曲
                        MainMusic.playLastMusic(self)
                     # 判断是否点击了下一曲 - 判断是否鼠标的坐标在暂停播放按钮的坐标范围内
                    elif NEXT_X <= mouse_x <= NEXT_X + MainMusic.theNext.rect.width and \
                        NEXT_Y <= mouse_y <= NEXT_Y + MainMusic.theNext.rect.height:
                        # 播放下一曲
                        MainMusic.playNextMusic(self)
                    # 判断是否点击了模式切换 - 判断是否鼠标的坐标在暂停播放按钮的坐标范围内
                    elif PLAY_PATTERN_X <= mouse_x <= PLAY_PATTERN_X + MainMusic.thePattern.rect.width and \
                        PLAY_PATTERN_Y <= mouse_y <= PLAY_PATTERN_Y + MainMusic.thePattern.rect.height:
                        # 改变播放模式
                        MainMusic.switchPattern(self)
                    # 判断是否点击了播放列表 - 判断是否鼠标的坐标在暂停播放按钮的坐标范围内
                    elif PLAYLIST_X <= mouse_x <= PLAYLIST_X + MainMusic.thePattern.rect.width and \
                        PLAYLIST_Y <= mouse_y <= PLAYLIST_Y + MainMusic.thePattern.rect.height:
                        # 播放下一曲
                        MainMusic.playNextMusic(self)
                    # 判断是否点击了音量按钮 - 判断是否鼠标的坐标在暂停播放按钮的坐标范围内
                    elif PLAYSOUND_X <= mouse_x <= PLAYSOUND_X + MainMusic.thePattern.rect.width and \
                        PLAYSOUND_Y <= mouse_y <= PLAYSOUND_Y + MainMusic.thePattern.rect.height:
                        # 调用音量增加函数
                        MainMusic.music.addVolume()
                        # # 调用音量降低函数
                        # MainMusic.music.subVolume()
                    # 判断是否点击了设置按钮 - 判断是否鼠标的坐标在暂停播放按钮的坐标范围内
                    elif PLAY_SETTING_X <= mouse_x <= PLAY_SETTING_X + MainMusic.thePattern.rect.width and \
                        PLAY_SETTING_Y <= mouse_y <= PLAY_SETTING_Y + MainMusic.thePattern.rect.height:
                        # 播放上一曲
                        self.playLastMusic()
                    # 进度条某位置 普通点击
                    if PROGRESS_BAR_X <= mouse_x <= PROGRESS_BAR_X + MainMusic.theProgressBar.rect.width and \
                        PROGRESS_BAR_Y <= mouse_y <= PROGRESS_BAR_Y + MainMusic.theProgressBar.rect.height:
                        # 计算新的开始时间
                        percentage = (mouse_x - PROGRESS_BAR_X) / MainMusic.theProgressBar.rect.width
                        MainMusic.startPos = int(percentage * MainMusic.musicTime)
                        # 更新标志
                        MainMusic.isUpdateTime = True
                        # 重新加载音乐 踩坑set_pos() - 播放时间会累计
                        pygame.mixer.music.play(start=MainMusic.startPos)  # 重新播放 加载新的位置

            # 2.2 键盘事件
            # 判断事件类型是否为按键按下，如果是，继续判断按键是哪一个按键，进行对应处理
            if event.type == pygame.KEYDOWN:
                # 判断具体是哪一个按键的处理
                if event.key == pygame.K_LEFT:  # 左方向键
                    print('上一曲')
                    # 播放上一曲
                    self.playLastMusic()
                elif event.key == pygame.K_RIGHT:  # 右方向键
                    print('下一曲')
                    # 播放下一曲
                    self.playNextMusic()
                elif event.key == pygame.K_UP:  # 上方向键
                    # 调用音量增加函数
                    MainMusic.music.addVolume()
                elif event.key == pygame.K_DOWN:  # 下方向键
                    # 调用音量降低函数
                    MainMusic.music.subVolume()
                elif event.key == pygame.K_SPACE:  # 空格键控制音乐播放
                    # 音乐播放/暂停 切换
                    MainMusic.playOrStop(self)
                elif event.key == pygame.K_TAB:  # Tab键控制音乐自动播放模式
                    # 自动播放模式切换
                    MainMusic.switchPattern(self)
                    # print("当前模式：", MainMusic.playPattern,"New:", MainMusic.newPattern)
            if event.type == pygame.KEYUP:
                pass

    # 结束使用
    def endUse(self):
        print('谢谢使用！')
        exit()  # 结束python解释器

    # 开始使用
    def startMusic(self):
        # 初始化
        pygame.init()
        # 设置图标
        icon = pygame.image.load('images/FMJJ.jpg')
        pygame.display.set_icon(icon)
        # 创建窗口加载窗口(借鉴官方文档)
        MainMusic.window = pygame.display.set_mode([MainMusic.SCREEN_WIDTH, MainMusic.SCREEN_HEIGHT])
        # 设置应用标题
        pygame.display.set_caption(VERSION)
        # 加载音乐到列表
        MainMusic.Musics_List = MainMusic.musicFromFile(self, FILENAME)
        # 获取随机列表
        MainMusic.shuffle_List = copy.deepcopy(MainMusic.Musics_List)  # 深拷贝
        random.shuffle(MainMusic.shuffle_List)  # shuffle打乱
        # 创建组件
        self.createComponent()
        # 默认音乐
        MainMusic.music = Music(MainMusic.Musics_List[MainMusic.musicNumber])
        # 播放音乐
        MainMusic.music.startPlay()
        # 关闭音乐
        MainMusic.music.playPause()
        # 改变播放状态
        MainMusic.isPlay = True
        # 让窗口持续刷新操作
        while True:
            # 给窗口一个填充色
            MainMusic.window.fill(COLOR_BACKGROUND)
            # 显示背景图片
            MainMusic.window.blit(BACKGROUND_IMAGE, (0, 0))
            # 显示图片
            MainMusic.window.blit(Singer_IMAGE, (16 * 2, 16 * 4))
            # 加载组件
            self.blitComponent()
            # 获取歌曲已经播放时间
            if MainMusic.isUpdateTime:
                # 算上更改前已经播放的时间
                MainMusic.playTime = MainMusic.startPos + pygame.mixer.music.get_pos() / 1000
            else:
                # 普通模式 走到底
                MainMusic.playTime = pygame.mixer.music.get_pos() / 1000
            # 自动切换下一首
            self.autoPlay()  # 根据模式播放
            # 在循坏中持续完成事件的获取
            self.getEvent()
            # 音乐信息 将绘制文字得到的小画布，放到窗口上
            MainMusic.window.blit(self.getTextSurface("本地音乐: %d"
                % len(MainMusic.Musics_List), THEME_FONT, SIZE_FONT, COLOR_FONT), (GETTEXT_X, GETTEXT_Y))
            # 音量信息 将绘制文字得到的小画布，放到窗口上
            MainMusic.window.blit(self.getTextSurface("音乐音量: %d"
                % MainMusic.VolumeValue, THEME_FONT, SIZE_FONT, COLOR_FONT), (VOLUME_X, VOLUME_Y))
            # 播放信息 将绘制文字得到的小画布，放到窗口上
            if MainMusic.playPattern == 2:  # 随机列表循环 实现随机播放
                MainMusic.window.blit(self.getTextSurface("%s" % MainMusic.shuffle_List[MainMusic.musicNumber][7:-4],
                    PLAY_FONT, PLAY_SIZE_FONT, COLOR_FONT), (PLAY_INFO_X, PLAY_INFO_Y))
            else:  # 默认列表循环
                MainMusic.window.blit(self.getTextSurface("%s" % MainMusic.Musics_List[MainMusic.musicNumber][7:-4],
                    PLAY_FONT, PLAY_SIZE_FONT, COLOR_FONT), (PLAY_INFO_X, PLAY_INFO_Y))
            # 音乐时长信息 将绘制文字得到的小画布，放到窗口上
            MainMusic.window.blit(self.getTextSurface(MainMusic.playTimeInfo.getStringOfTime(MainMusic.playTime),
                THEME_FONT, TIME_SIZE_FONT, COLOR_FONT), (TIME_X, TIME_Y))
            MainMusic.window.blit(self.getTextSurface(MainMusic.musicTimeInfo.timeString,
                THEME_FONT, TIME_SIZE_FONT, COLOR_FONT), (TIME_X + 16 * 28 + 11, TIME_Y))  # 像素点位置
            # 暴力延时
            # time.sleep(DELAY)  # 延时 DELAYs
            # 窗口的刷新
            pygame.display.update()


if __name__ == '__main__':
    MainMusic().startMusic()  # 开始运行
