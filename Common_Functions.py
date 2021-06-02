import win32gui

import numpy as np
from PIL import ImageGrab
import cv2

import pynput

from time import sleep

mouse_drag = pynput.mouse.Controller()
mouse_button = pynput.mouse.Button

# 공통 함수

# position = 좌표
def Click(position):
    mouse_drag.position=(position) # 정해진 좌표로 마우스 이동
    mouse_drag.press(mouse_button.left) # 마우스 왼쪽 클릭 후 유지
    mouse_drag.release(mouse_button.left) # 마우스 왼쪽 클릭 해제

# 마우스 드래그
def Drag(window):
    position = Search_image_on_image(window,'baccarat_classic.png',0.9)
    if position is not None :
        from_x,from_y = position
        x = 0

        mouse_drag.position = (from_x, from_y)
        mouse_drag.press(mouse_button.left)
        while x<500:
            mouse_drag.position=(from_x-x, from_y)
            x+=1
            sleep(0.001)
        sleep(0.25)
        mouse_drag.release(mouse_button.left)
    
# 윈도우 이미지 위에서 이미지를 찾음
def Search_image_on_image(window,template,threshold=1) :

    hwnd = win32gui.FindWindow(None, window)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    img = np.array(ImageGrab.grab((left, top, right, bot)))
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    template = cv2.imread(template)
    w, h = template.shape[:-1]

    try :
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    except :
        print('Error : Window창을 감지할 수 없습니다.')
        return None

    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):  # Switch collumns and rows
        return (int(w / 2 + pt[0])+left,int(h / 2 + pt[1])+top)

    return None