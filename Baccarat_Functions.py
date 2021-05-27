from PIL import ImageGrab
import cv2
import numpy as np
import pytesseract

import win32gui

from time import sleep

import re

from Common_Functions import Search_image_on_image, Click

# 바카라 전용 함수

# 첫방 번호 확인하기
def Baccarat_First_room_check(window):
    hwnd = win32gui.FindWindow(None, window)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)

    room_number = np.array(ImageGrab.grab((left+350, top+60, left+450, top+85)))
    room_number = cv2.cvtColor(room_number,cv2.COLOR_BGR2RGB)

    return room_number

# 한사이클 돌았는지 매번 확인
def Baccarat_Room_check(window,template,threshold=1):
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

# 유저이름 확인
def Baccarat_Check_user_name(window):
    hwnd = win32gui.FindWindow(None, window)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)

    for num in range(1,8):
        print('바카라 '+str(num)+'번 유저 닉네임 확인')
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

        if len(color_text) > 1 and len(color_text) < 9 :
            print('color :',color_text)
        if len(gray_text) > 1 and len(gray_text) < 9 :
            print('gray :',gray_text)


# ==================================================================================================================
# ==================================================================================================================
# ==================================================================================================================
# ==================================================================================================================


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

                print('입장 완료')
                # 입장했다면 방 번호 확인
                while True :
                    baccart_enter_check = Search_image_on_image(window,'baccart_enter_check.png',0.9)
                    if baccart_enter_check is not None :
                        sleep(2)
                        print('바카라 처음 입장한 방 번호 등록 중...')
                        room_number = Baccarat_First_room_check(window)
                        one_cycle = False

                        sleep(1)
                        print('바카라 처음 입장 방 등록 완료')

                        while True :
                            print('바카라 처음 방으로 돌아왔는지 확인')
                            baccarat_room_check = Baccarat_Room_check(window,room_number,0.98)
                            
                            #한사이클 돌았다면 방 나가기
                            if baccarat_room_check is not None and one_cycle:
                                print('바카라 스캐닝 종료 중...')
                                while True :
                                    menu_button = Search_image_on_image(window,'baccarat_menu.png',0.9)
                                    if menu_button is not None:
                                        Click(menu_button)
                                        sleep(1)
                                        while True :
                                            exit_button = Search_image_on_image(window,'baccarat_exit.png',0.9)
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
                                while True :
                                    next_button = Search_image_on_image(window,'next_button.png',0.9)
                                    if next_button is not None :
                                        Baccarat_Check_user_name(window)
                                        Click(next_button)
                                        while True :
                                            next_room_button = Search_image_on_image(window,'next_room.png',0.9)
                                            if next_room_button is not None :
                                                # sleep(0.25)
                                                print('바카라 다음 방 이동')
                                                Click(next_room_button)
                                                one_cycle = True
                                                break
                                        sleep(1)
                                        break
                        break
                break

        while True :
            back_button = Search_image_on_image(window,'back.png',0.9)
            if back_button is not None :
                print('바카라 스캐닝 종료 완료')
                Click(back_button)
                break