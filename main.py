from time import sleep

from Holdom_Functions import Play_holdom
from Baccarat_Functions import Play_baccarat
from Common_Functions import Drag

if __name__ == '__main__':
    window = "LDPlayer"

    while True :

        # 홀덤 클릭
        Play_holdom(window,'holdom',False,True)

        # sleep(2)

        # # 바카라 타이거6
        # print('Baccarat Tiger 입장 중...')
        # Play_baccarat(window,'baccarat_tiger',True,True)

        # sleep(2)

        # # 바카라 클래식
        # print('Baccarat Classic 입장 중..')
        # Play_baccarat(window,'baccarat_classic',True,True)

        # sleep(2)

        # Drag(window)

        # # 바카라 블랙잭
        # blackjack = Search_image_on_image(window,'blackjack.png',0.9)
        # if blackjack is not None :
        #     Click(blackjack)
 
        # sleep(2)

        # # 마우스 드래그
        # Drag(window)

        # # 바카라 파블로스
        # print('Baccarat Pabulos 입장 중...')
        # Play_baccarat(window,'baccarat_fabulos',True,True)
        
        # sleep(2)