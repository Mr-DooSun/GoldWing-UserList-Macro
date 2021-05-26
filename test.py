import win32gui

from PIL import ImageGrab

import numpy as np
import cv2

import re

import pynput

import pytesseract

from time import sleep

mouse_drag = pynput.mouse.Controller()
mouse_button = pynput.mouse.Button

# ======================================================================================
# ======================================================================================
# ======================================================================================

# 공통 함수

# position = 좌표
def Click(position):
    mouse_drag.position=(position) # 정해진 좌표로 마우스 이동
    mouse_drag.press(mouse_button.left) # 마우스 왼쪽 클릭 후 유지
    mouse_drag.release(mouse_button.left) # 마우스 왼쪽 클릭 해제

# 마우스 드래그
def Drag(window):
    position = Search_image_on_image(window,'baccarat_fabulos.png',0.9)
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

# =====================================================================================
# =====================================================================================
# =====================================================================================

# 바카라 전용 함수

# 한사이클 돌았는지 매번 확인
def Room_check(window,template,threshold=1):
    hwnd = win32gui.FindWindow(None, window)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    img = np.array(ImageGrab.grab((left, top, right, bot)))
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

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

# 첫방 번호 확인하기
def First_room_check(window):
    hwnd = win32gui.FindWindow(None, window)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)

    room_number = np.array(ImageGrab.grab((left+350, top+60, left+450, top+85)))
    room_number = cv2.cvtColor(room_number,cv2.COLOR_BGR2RGB)

    return room_number

# 유저이름 확인
def Check_user_name(window):
    hwnd = win32gui.FindWindow(None, window)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)

    for num in range(1,8):
        if num is 1 :
            img = np.array(ImageGrab.grab((left+82, top+579, left+232, top+606)))
        elif num is 2 :
            img = np.array(ImageGrab.grab((left+275, top+708, left+425, top+735)))
        elif num is 3 :
            img = np.array(ImageGrab.grab((left+510, top+766, left+660, top+793)))
        elif num is 4 :
            img = np.array(ImageGrab.grab((left+750, top+772, left+900, top+802)))
        elif num is 5 :
            img = np.array(ImageGrab.grab((left+985, top+766, left+1135, top+793)))
        elif num is 6 :
            img = np.array(ImageGrab.grab((left+1225, top+706, left+1375, top+734)))
        elif num is 7:
            img = np.array(ImageGrab.grab((left+1418, top+576, left+1568, top+604)))

        color = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        color_text = pytesseract.image_to_string(color,lang="kor+eng")
        color_text = re.sub('[^0-9a-zA-Zㄱ-힗]', '', color_text)

        gray_text = pytesseract.image_to_string(gray,lang="kor+eng")
        gray_text = re.sub('[^0-9a-zA-Zㄱ-힗]', '', gray_text)

        if len(color_text) > 1 :
            print('color :',color_text)
        if len(gray_text) > 1 :
            print('gray :',gray_text)


# ======================================================================================
# ======================================================================================
# ======================================================================================

# 바카라 타이거 사이클
def Bakara_Cycle(window,bakara_name) :
    bakara = Search_image_on_image(window,bakara_name+'.png',0.9)
    if bakara is not None :
        Click(bakara)
        
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
                        sleep(3)
                        room_number = First_room_check(window)
                        one_cycle = False

                        sleep(1)

                        while True :
                            room_check = Room_check(window,room_number,0.98)
                            
                            #한사이클 돌았다면 방 나가기
                            if room_check is not None and one_cycle:
                                menu_button = Search_image_on_image(window,'menu.png',0.9)
                                while True : 
                                    if menu_button is not None:
                                        Click(menu_button)
                                        while True :
                                            exit_button = Search_image_on_image(window,'exit.png',0.9)
                                            if exit_button is not None:
                                                Click(exit_button)
                                                while True :
                                                    access_button = Search_image_on_image(window,'access.png',0.9)
                                                    if access_button is not None :
                                                        Click(access_button)
                                                        break
                                                break
                                            else :
                                                Click(menu_button)
                                        break
                                break
                            
                            # 한사이클이 안돌았다면 사용자 이름 확인하기
                            else :
                                next_button = Search_image_on_image(window,'next_button.png',0.9)
                                if next_button is not None :
                                    Check_user_name(window)
                                    Click(next_button)
                                    while True :
                                        next_room_button = Search_image_on_image(window,'next_room.png',0.9)
                                        if next_room_button is not None :
                                            # sleep(0.25)
                                            Click(next_room_button)
                                            one_cycle = True
                                            break
                                    sleep(1)
                        break
                break

        while True :
            back_button = Search_image_on_image(window,'back.png',0.9)
            if back_button is not None :
                Click(back_button)
                break

# =====================================================================================
# =====================================================================================
# =====================================================================================

if __name__ == '__main__':
    room_number = None

    while True :
        window = "LDPlayer"

        holdom = None
        blackjack = None

        # 홀덤
        holdom = Search_image_on_image(window,'holdom.png',0.9)
        if holdom is not None :
            Click(holdom)
            while True :
                gold_holdom = Search_image_on_image(window,'gold_holdom.png',0.9)
                

        # # 바카라 타이거6
        # print('Baccarat Tiger Scanning ..')
        # Bakara_Cycle(window,'baccarat_tiger')

        # sleep(2)

        # # 바카라 파블로스
        # print('Baccarat Pabulos Scanning ..')
        # Bakara_Cycle(window,'baccarat_fabulos')

        # sleep(2)

        # Drag(window)

        # # 바카라 블랙잭
        # blackjack = Search_image_on_image(window,'blackjack.png',0.9)
        # if blackjack is not None :
        #     Click(blackjack)

        # sleep(2)

        # # 마우스 드래그
        # Drag(window)
        # # 바카라 클래식
        # print('Baccarat Cycle Scanning ..')
        # Bakara_Cycle(window,'baccarat_classic')
        
        sleep(0.5)