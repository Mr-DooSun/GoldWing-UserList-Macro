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

# 홀덤 전용 함수

# 홀덤 첫방 번호 확인
def Holdom_First_room_check(window):
    hwnd = win32gui.FindWindow(None, window)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)

    room_number = np.array(ImageGrab.grab((left+1390, top+60, left+1480, top+85))) 
    room_number = cv2.cvtColor(room_number,cv2.COLOR_BGR2RGB)

    return room_number

# 홀덤 한사이클 돌았는지 확인
def Holdom_Room_check(window,template,threshold=1):
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

# 착석 확인 하기
def Sit_check(window,template,num,threshold=1):
    start_location = [(345,75),(130,220),(65,440),(130,665),(600,705),(1415,665),(1480,445),(1415,220),(1190,85)]
    end_location = [(420,130),(195,260),(135,485),(195,710),(670,750),(1480,710),(1545,485),(1480,260),(1255,130)]
    start_x,start_y = start_location[num-1]
    end_x,end_y = end_location[num-1]

    hwnd = win32gui.FindWindow(None, window)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    img = np.array(ImageGrab.grab((left+start_x, top+start_y, left+end_x, top+end_y)))
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

def Holdom_Check_user_name(window):
    hwnd = win32gui.FindWindow(None, window)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)

    click_list = [(350,100),(105,235),(60,490),(125,725),(600,765),(1475,675),(1540,455),(1480,225),(1240,90)]
    user_name_list = [(455,80,685,127),(251,163,481,210),(91,220,321,267),(95,460,326,507),(508,498,738,545),(1163,498,1393,545),(1177,345,1407,392),(1132,193,1362,240),(1013,83,1240,130)]
    for num in range(1,10):
        img = None
        start_x,start_y,end_x,end_y = user_name_list[num-1]
        # holdom 1
        if num is 1 :
            print(num)
            sit_check_button = Sit_check(window,'sit_check.png',num,0.8)
            if sit_check_button is not None :
                pass
            else :
                Click(click_list[num-1])
                while True :
                    user_inform_check = Search_image_on_image(window,'user_inform_check.png',0.9)
                    if user_inform_check is not None :
                        img = np.array(ImageGrab.grab((left+start_x, top+start_y, left+end_x, top+end_y)))
                        break

        # holdom 2 이상
        elif num > 1 :
            print(num)
            sit_check_button = Sit_check(window,'sit_check.png',num,0.8)
            if sit_check_button is not None :
                pass
            else :
                Click(click_list[num-1])
                Click(click_list[num-1])
                while True :
                    user_inform_check = Search_image_on_image(window,'user_inform_check.png',0.9)
                    if user_inform_check is not None :
                        img = np.array(ImageGrab.grab((left+start_x, top+start_y, left+end_x, top+end_y)))
                        break
        
        if img is not None : 
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

# =====================================================================================
# =====================================================================================
# =====================================================================================

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

        if len(color_text) > 1 and len(color_text) < 9 :
            print('color :',color_text)
        if len(gray_text) > 1 and len(gray_text) < 9 :
            print('gray :',gray_text)


# ======================================================================================
# ======================================================================================
# ======================================================================================

# 홀덤 사이클
def Holdom_Cycle(window,holdom_name) :
    holdom = Search_image_on_image(window,holdom_name+'.png',0.9)
    if holdom is not None :
        Click(holdom)
        sleep(1)

        # 홀덤 콜드 클릭
        while True :
            gold_holdom = Search_image_on_image(window,'gold_holdom.png',0.9)
            if gold_holdom is not None :
                Click(gold_holdom)
                
                sleep(1)
                # 채널선택 클릭
                while True :
                    chose_channel = Search_image_on_image(window,'chose_channel.png',0.98)
                    if chose_channel is not None:
                        Click(chose_channel)

                        sleep(1)
                        # 홀덤 1번째 입장하기 버튼이 있다면 클릭  
                        while True :
                            enter = Search_image_on_image(window,'enter.png',0.9)
                            if enter is not None :
                                Click(enter)
                                
                                sleep(0.5)
                                # 홀덤 2번째 입장하기 버튼이 있다면 클릭 
                                while True :
                                    enter_access = Search_image_on_image(window,'enter_access.png',0.9)
                                    if enter_access is not None :
                                        Click(enter_access)
                                        
                                        # 홀덤 방에 제대로 입장 했다면 방번호 확인 
                                        while True :
                                            holdom_enter_check = Search_image_on_image(window,'holdom_enter_check.png',0.9)
                                            if holdom_enter_check is not None :
                                                sleep(2)
                                                room_number = Holdom_First_room_check(window)
                                                one_cycle = False
                                                sleep(1)

                                                # 한사이클 돌았는지 확인
                                                while True:
                                                    holdom_room_check = Holdom_Room_check(window,room_number,0.98)

                                                    # 한사이클을 돌았다면 방 나가기
                                                    if holdom_room_check is not None and one_cycle:
                                                        while True :
                                                            menu_button = Search_image_on_image(window,'holdom_menu.png',0.9)
                                                            if menu_button is not None :
                                                                Click(menu_button)
                                                                sleep(1)
                                                                while True :
                                                                    exit_button = Search_image_on_image(window,'holdom_exit.png',0.9)
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
                                                    # 한사이클을 안돌았다면, 
                                                    else :
                                                        while True :
                                                            menu_button = Search_image_on_image(window,'holdom_menu.png',0.9)
                                                            if menu_button is not None :
                                                                Holdom_Check_user_name(window)
                                                                Click(menu_button)
                                                                while True :
                                                                    next_room_button = Search_image_on_image(window,'holdom_next_room.png',0.9)
                                                                    if next_room_button is not None :
                                                                        # sleep(0.25)
                                                                        Click(next_room_button)
                                                                        one_cycle = True
                                                                        break
                                                                sleep(1)
                                                                break
                                                break
                                        break
                                break
                        break
                break 

        while True :
            back_button = Search_image_on_image(window,'back.png',0.9)
            if back_button is not None :
                Click(back_button)
                sleep(1)
                while True :
                    return_button = Search_image_on_image(window,'return.png',0.9)
                    if return_button is not None:
                        Click(return_button)
                        break
                break

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
                    baccart_enter_check = Search_image_on_image(window,'baccart_enter_check.png',0.9)
                    if baccart_enter_check is not None :
                        sleep(2)
                        room_number = Baccarat_First_room_check(window)
                        one_cycle = False

                        sleep(1)

                        while True :
                            baccarat_room_check = Baccarat_Room_check(window,room_number,0.98)
                            
                            #한사이클 돌았다면 방 나가기
                            if baccarat_room_check is not None and one_cycle:
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

        # 홀덤 클릭
        print('Holdom Scanning ..')
        Holdom_Cycle(window,'holdom')

        sleep(2)

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
        # print('Baccarat Classic Scanning ..')
        # Bakara_Cycle(window,'baccarat_classic')
        
        # sleep(0.5)