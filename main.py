from time import sleep

from Holdom_Functions import Holdom_Cycle
from Baccarat_Functions import Bakara_Cycle

# =====================================================================================
# =====================================================================================
# =====================================================================================

if __name__ == '__main__':
    room_number = None

    while True :
        window = "LDPlayer"

        holdom = None
        blackjack = None

        # # 홀덤 클릭
        print('Holdom Scanning ..')
        Holdom_Cycle(window,'holdom')

        sleep(2)

        # 바카라 타이거6
        print('Baccarat Tiger Scanning ..')
        Bakara_Cycle(window,'baccarat_tiger')

        sleep(2)

        # 바카라 파블로스
        print('Baccarat Pabulos Scanning ..')
        Bakara_Cycle(window,'baccarat_fabulos')

        sleep(2)

        # Drag(window)

        # # 바카라 블랙잭
        # blackjack = Search_image_on_image(window,'blackjack.png',0.9)
        # if blackjack is not None :
        #     Click(blackjack)

        # sleep(2)

        # 마우스 드래그
        Drag(window)
        # 바카라 클래식
        print('Baccarat Classic Scanning ..')
        Bakara_Cycle(window,'baccarat_classic')
        
        sleep(0.5)