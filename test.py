import win32gui

from PIL import ImageGrab

import numpy as np
import cv2

import pynput

import pytesseract

mouse_drag = pynput.mouse.Controller()
mouse_button = pynput.mouse.Button

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

# position = 좌표
def Click(position):
    mouse_drag.position=(position) # 정해진 좌표로 마우스 이동
    mouse_drag.press(mouse_button.left) # 마우스 왼쪽 클릭 후 유지
    mouse_drag.release(mouse_button.left) # 마우스 왼쪽 클릭 해제

def Check_text(img):
    pass

if __name__ == '__main__':
    while True :
        window = "LDPlayer"

        holdom = None
        bakara_tiger = None
        baccarat_fabulos = None
        blackjack = None
        baccarat_classic = None

        # # 홀덤
        # holdom = Search_image_on_image(window,'holdom.png',0.9)
        # if holdom is not None :
        #     Click(holdom)

        # 바카라 타이거6
        bakara_tiger = Search_image_on_image(window,'baccarat_tiger.png',0.9)
        if bakara_tiger is not None :
            Click(bakara_tiger)
            
            # 입장 버튼이 있는지 확인
            while True :
                enter = Search_image_on_image(window,'enter.png',0.9)
                # 입장 버튼이 있다면 입장하기
                if enter is not None :
                    Click(enter)
                    
                    # 입장했는지 확인
                    while True :
                        enter_check = Search_image_on_image(window,'enter_check.png',0.9)
                        
                        if enter_check is not None :
                            hwnd = win32gui.FindWindow(None, window)
                            left, top, right, bot = win32gui.GetWindowRect(hwnd)
                            img = np.array(ImageGrab.grab((left+76, top+470, left+176, top+491)))
                            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

                            break
                    break

        # # 바카라 파블러스
        # baccarat_fabulos = Search_image_on_image(window,'baccarat_fabulos.png',0.9)
        # if baccarat_fabulos is not None :
        #     Click(baccarat_fabulos)

        # # 바카라 블랙잭
        # blackjack = Search_image_on_image(window,'blackjack.png',0.9)
        # if blackjack is not None :
        #     Click(blackjack)

        # # 바카라 클래식
        # baccarat_classic = Search_image_on_image(window,'baccarat_classic.png',0.9)
        # if baccarat_classic is not None :
        #     Click(baccarat_classic)