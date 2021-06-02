from time import sleep

import win32gui

from PIL import ImageGrab
import cv2
import numpy as np
import pytesseract

import re

from Common_Functions import Search_image_on_image, Click

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

def Channel_check(window):
    hwnd = win32gui.FindWindow(None, window)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)

    max_channel_number = np.array(ImageGrab.grab((left+1245, top+175, left+1295, top+225)))
    max_channel_number = cv2.cvtColor(max_channel_number,cv2.COLOR_BGR2RGB)

    now_channel_number = np.array(ImageGrab.grab((left+1220, top+185, left+1240, top+215))) 
    now_channel_number = cv2.cvtColor(now_channel_number,cv2.COLOR_BGR2RGB)

    w, h = now_channel_number.shape[:-1]

    try :
        res = cv2.matchTemplate(max_channel_number, now_channel_number, cv2.TM_CCOEFF_NORMED)
    except :
        print('Error : Window창을 감지할 수 없습니다.')
        return None

    loc = np.where(res >= 0.9)

    for pt in zip(*loc[::-1]):  # Switch collumns and rows
        return (int(w / 2 + pt[0])+left,int(h / 2 + pt[1])+top)

    return None

# 홀덤 유저 이름 찾기
def Holdom_Check_user_name(window):
    hwnd = win32gui.FindWindow(None, window)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)

    click_list = [(350,100),(105,235),(60,490),(125,725),(600,765),(1475,675),(1540,455),(1480,225),(1240,90)]
    user_name_list = [(455,80,685,127),(251,163,481,210),(91,220,321,267),(95,460,326,507),(508,498,738,545),(1163,498,1393,545),(1177,345,1407,392),(1132,193,1362,240),(1013,83,1240,130)]
    num = 1
    while num < 10 :
        img = None
        start_x,start_y,end_x,end_y = user_name_list[num-1]
        # holdom 1
        if num is 1 :
            print('홀덤 '+str(num)+'번 착석 확인')
            sit_check_button = Sit_check(window,'sit_check.png',num,0.8)
            if sit_check_button is not None :
                pass
            else :
                Click(click_list[num-1])
                sleep(1)
                while True :
                    user_inform_check = Search_image_on_image(window,'user_inform_check.png',0.9)
                    if user_inform_check is not None :
                        img = np.array(ImageGrab.grab((left+start_x, top+start_y, left+end_x, top+end_y)))
                        sleep(1)
                        Click(click_list[num-1])
                        break
                    else :
                        num-=1
                        break

        # holdom 2 이상
        elif num > 1 :
            print('홀덤 '+str(num)+'번 착석 확인 및 유저 닉네임 확인')
            sit_check_button = Sit_check(window,'sit_check.png',num,0.8)
            if sit_check_button is not None :
                pass
            else :
                Click(click_list[num-1])
                sleep(1)
                while True :
                    user_inform_check = Search_image_on_image(window,'user_inform_check.png',0.9)
                    if user_inform_check is not None :
                        img = np.array(ImageGrab.grab((left+start_x, top+start_y, left+end_x, top+end_y)))
                        sleep(1)
                        Click(click_list[num-1])
                        break
                    else :
                        num-=1
                        break
        
        if img is not None : 
            color = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            upper_blue = (200, 240, 255) # hsv 이미지에서 바이너리 이미지로 생성 , 적당한 값 30
            lower_blue = (141, 163, 174)

            img_mask = cv2.inRange(color, lower_blue, upper_blue)
            
            color_text = pytesseract.image_to_string(color,lang="kor+eng")
            color_text = re.sub('[^0-9a-zA-Zㄱ-힗]', '', color_text)

            gray_text = pytesseract.image_to_string(gray,lang="kor+eng")
            gray_text = re.sub('[^0-9a-zA-Zㄱ-힗]', '', gray_text)

            img_mask_text = pytesseract.image_to_string(img_mask,lang='kor+eng')
            img_mask_text = re.sub('[^0-9a-zA-Zㄱ-힗]', '', img_mask_text)

            if len(img_mask_text) > 1 and len(img_mask_text) < 9 :
                print('img_maks_text :',img_mask_text)
            else : 
                if len(color_text) > 1 and len(color_text) < 9 :
                    print('color :',color_text)
                if len(gray_text) > 1 and len(gray_text) < 9 :
                    print('gray :',gray_text)
        num += 1


# ==================================================================================================================
# ==================================================================================================================
# ==================================================================================================================
# ==================================================================================================================


# 홀덤 사이클
def Holdom_Cycle(window) :
    enter_list=[(725,375),(1135,375),(1545,375),
            (705,585),(1115,585),(1525,585),
            (685,790),(1095,790),(1505,790)]
    nexting = False
    while True :
        # 홀덤 1번째 입장하기 버튼이 있다면 클릭
        for enter in enter_list :
            if nexting :
                holdom_next_channel = Search_image_on_image(window,'holdom_next_channel.png',0.9)
                if holdom_next_channel is not None :
                    Click(holdom_next_channel)
                    sleep(2)

            Click(enter)
            
            sleep(1)
            # 홀덤 2번째 입장하기 버튼이 있다면 클릭 
            while True :
                enter_access = Search_image_on_image(window,'enter_access.png',0.9)
                if enter_access is not None :
                    Click(enter_access)
                    print('홀덤 입장 완료')
                    # 입장했는지 확인
                    while True :
                        holdom_enter_check = Search_image_on_image(window,'holdom_enter_check.png',0.9)
                        if holdom_enter_check is not None :
                            # 유저이름 확인
                            Holdom_Check_user_name(window)
                            sleep(1)
                            # 메뉴버튼 클릭
                            while True :
                                menu_button = Search_image_on_image(window,'holdom_menu.png',0.9)
                                if menu_button is not None :
                                    Click(menu_button)
                                    sleep(1)
                                    # 방나가기 버튼 클릭
                                    while True :
                                        exit_button = Search_image_on_image(window,'holdom_exit.png',0.9)
                                        if exit_button is not None:
                                            Click(exit_button)
                                            # 나가기 확인 버튼 클릭
                                            while True :
                                                access_button = Search_image_on_image(window,'access.png',0.9)
                                                if access_button is not None :
                                                    Click(access_button)
                                                    sleep(3)
                                                    break
                                            break
                                        else :
                                            Click(menu_button)
                                    break
                            break
                    break
                not_enter = Search_image_on_image(window,'holdom_not_enter.png',0.9)
                if not_enter is not None :
                    Click(not_enter)
                    sleep(2)
                    break
                
                else :
                    break

        sleep(2)

        if Channel_check(window) is None:
            while True :
                holdom_next_channel = Search_image_on_image(window,'holdom_next_channel.png',0.9)
                if holdom_next_channel is not None :
                    Click(holdom_next_channel)
                    nexting = True
                    break
        else :
            break

def Play_holdom(window,holdom_name,master_channel,vip_channel):
    holdom = Search_image_on_image(window,holdom_name+'.png',0.9)
    if holdom is not None :
        Click(holdom)
        sleep(1)

        # 홀덤 콜드 클릭
        while True :
            gold_holdom = Search_image_on_image(window,'gold_holdom.png',0.9)
            if gold_holdom is not None :
                print('홀덤 입장 중...')
                Click(gold_holdom)
                
                sleep(1)
                # 채널선택 클릭
                while True :
                    chose_channel = Search_image_on_image(window,'chose_channel.png',0.98)
                    if chose_channel is not None:
                        Click(chose_channel)

                        sleep(1)
                        
                        break
                break
        
        if master_channel :
            while True :
                change_channel = Search_image_on_image(window,'change_channel.png',0.9)
                if change_channel is not None :
                    Click(change_channel)
                    while True :
                        master_channel = Search_image_on_image(window,'master_channel.png',0.9)
                        if master_channel is not None :
                            Click(master_channel)
                            break
                    break
            Holdom_Cycle(window)

        if vip_channel :
            while True :
                change_channel = Search_image_on_image(window,'change_channel.png',0.9)
                if change_channel is not None :
                    Click(change_channel)
                    while True :
                        vip_channel = Search_image_on_image(window,'vip_channel.png',0.9)
                        if vip_channel is not None :
                            Click(vip_channel)
                            break
                    break
            Holdom_Cycle(window)

        while True :
                back_button = Search_image_on_image(window,'back.png',0.9)
                if back_button is not None :
                    Click(back_button)
                    sleep(1)
                    while True :
                        return_button = Search_image_on_image(window,'return.png',0.9)
                        if return_button is not None:
                            print('홀덤 스캐닝 종료 완료')
                            Click(return_button)
                            break
                    break

# window = 'LDPlayer'
# hwnd = win32gui.FindWindow(None, window)
# left, top, right, bot = win32gui.GetWindowRect(hwnd)

# now_channel_number = np.array(ImageGrab.grab((left+1245, top+175, left+1295, top+225))) 
# now_channel_number = cv2.cvtColor(now_channel_number,cv2.COLOR_BGR2RGB)

# cv2.imshow('imgaeg',now_channel_number)
# cv2.waitKey(0)

# Holdom_Cycle('LDPlayer')