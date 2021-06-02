from PyQt5 import QtCore, QtGui, QtWidgets

from time import sleep

from Holdom_Functions import Play_holdom
from Baccarat_Functions import Play_baccarat
from Common_Functions import Drag

import threading

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("GoldWing Macro")
        MainWindow.setFixedSize(300, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 배달의 민족 연성체
        self.new_font = QtGui.QFontDatabase()
        self.new_font.addApplicationFont('BMYEONSUNG.ttf')

        #Title_Label
        self.Title_label = QtWidgets.QLabel(self.centralwidget)
        self.Title_label.setGeometry(QtCore.QRect(60, 30, 300, 40))
        self.Title_label.setObjectName("Title_label")
        self.Title_label.setText('GoldWing Macro')
        self.Title_label.setFont(QtGui.QFont('배달의민족 연성',20))

        # ================================================================

        # 홀덤
        self.holdom_label = QtWidgets.QLabel(self.centralwidget)
        self.holdom_label.setGeometry(QtCore.QRect(40, 100, 56, 30))
        self.holdom_label.setObjectName("holdom_label")
        self.holdom_label.setText("홀덤")
        self.holdom_label.setFont(QtGui.QFont('배달의민족 연성',20))

        # 홀덤_MASTER
        self.holdom_master = QtWidgets.QCheckBox(self.centralwidget)
        self.holdom_master.setGeometry(QtCore.QRect(70,140,60,20))
        self.holdom_master.setText("마스터")
        self.holdom_master.setFont(QtGui.QFont('배달의민족 연성',14))

        # 홀덤_VIP
        self.holdom_vip = QtWidgets.QCheckBox(self.centralwidget)
        self.holdom_vip.setGeometry(QtCore.QRect(170,140,60,20))
        self.holdom_vip.setText("VIP")
        self.holdom_vip.setFont(QtGui.QFont('배달의민족 연성',14))

        # ================================================================

        # 바카라 - 타이거
        self.tiger_label = QtWidgets.QLabel(self.centralwidget)
        self.tiger_label.setGeometry(QtCore.QRect(40, 180, 150, 30))
        self.tiger_label.setObjectName("tiger_label")
        self.tiger_label.setText("바카라 - 타이거")
        self.tiger_label.setFont(QtGui.QFont('배달의민족 연성',20))

        # 바카라 - 타이거_MASTER
        self.tiger_master = QtWidgets.QCheckBox(self.centralwidget)
        self.tiger_master.setGeometry(QtCore.QRect(70,220,60,20))
        self.tiger_master.setText("마스터")
        self.tiger_master.setFont(QtGui.QFont('배달의민족 연성',14))

        # 바카라 - 타이거_VIP
        self.tiger_vip = QtWidgets.QCheckBox(self.centralwidget)
        self.tiger_vip.setGeometry(QtCore.QRect(170,220,60,20))
        self.tiger_vip.setText("VIP")
        self.tiger_vip.setFont(QtGui.QFont('배달의민족 연성',14))

        # ================================================================
        
        # 바카라 - 클래식
        self.classic_label = QtWidgets.QLabel(self.centralwidget)
        self.classic_label.setGeometry(QtCore.QRect(40, 260, 150, 30))
        self.classic_label.setObjectName("classic_label")
        self.classic_label.setText("바카라 - 클래식")
        self.classic_label.setFont(QtGui.QFont('배달의민족 연성',20))

        # 바카라 - 클래식_MASTER
        self.classic_master = QtWidgets.QCheckBox(self.centralwidget)
        self.classic_master.setGeometry(QtCore.QRect(70,300,60,20))
        self.classic_master.setText("마스터")
        self.classic_master.setFont(QtGui.QFont('배달의민족 연성',14))

        # 바카라 - 클래식_VIP
        self.classic_vip = QtWidgets.QCheckBox(self.centralwidget)
        self.classic_vip.setGeometry(QtCore.QRect(170,300,60,20))
        self.classic_vip.setText("VIP")
        self.classic_vip.setFont(QtGui.QFont('배달의민족 연성',14))

        # ================================================================

        # 블랙잭
        self.blackjack_label = QtWidgets.QLabel(self.centralwidget)
        self.blackjack_label.setGeometry(QtCore.QRect(40, 340, 150, 30))
        self.blackjack_label.setObjectName("blackjack_label")
        self.blackjack_label.setText("블랙잭")
        self.blackjack_label.setFont(QtGui.QFont('배달의민족 연성',20))

        # 블랙잭 - MASTER
        self.blackjack_master = QtWidgets.QCheckBox(self.centralwidget)
        self.blackjack_master.setGeometry(QtCore.QRect(70,380,60,20))
        self.blackjack_master.setText("마스터")
        self.blackjack_master.setFont(QtGui.QFont('배달의민족 연성',14))

        # 블랙잭 - VIP
        self.blackjack_vip = QtWidgets.QCheckBox(self.centralwidget)
        self.blackjack_vip.setGeometry(QtCore.QRect(170,380,60,20))
        self.blackjack_vip.setText("VIP")
        self.blackjack_vip.setFont(QtGui.QFont('배달의민족 연성',14))

        # ================================================================

        # 바카라 - 파블로스4
        self.fabulos_label = QtWidgets.QLabel(self.centralwidget)
        self.fabulos_label.setGeometry(QtCore.QRect(40, 420, 180, 30))
        self.fabulos_label.setObjectName("fabulos_label")
        self.fabulos_label.setText("바카라 - 파블로스4")
        self.fabulos_label.setFont(QtGui.QFont('배달의민족 연성',20))

        # 바카라 - 파블로스4_MASTER
        self.fabulos_master = QtWidgets.QCheckBox(self.centralwidget)
        self.fabulos_master.setGeometry(QtCore.QRect(70,460,60,20))
        self.fabulos_master.setText("마스터")
        self.fabulos_master.setFont(QtGui.QFont('배달의민족 연성',14))

        # 바카라 - 파블로스4_VIP
        self.fabulos_vip = QtWidgets.QCheckBox(self.centralwidget)
        self.fabulos_vip.setGeometry(QtCore.QRect(170,460,60,20))
        self.fabulos_vip.setText("VIP")
        self.fabulos_vip.setFont(QtGui.QFont('배달의민족 연성',14))

        # ================================================================

        # 시작 중지
        self.Start_or_Stop = False

        # START 버튼
        self.start_Button = QtWidgets.QPushButton(self.centralwidget)
        self.start_Button.setGeometry(QtCore.QRect(90, 520, 120, 35))
        self.start_Button.setObjectName("start_Button")
        self.start_Button.clicked.connect(self.button_click_event)
        self.start_Button.setText("START")
        self.start_Button.setFont(QtGui.QFont('배달의민족 연성',13))

        # ================================================================

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.Playing_thread()

    def Playing(self, MainWindow):
        window = "LDPlayer"
        while True :
            while self.Start_or_Stop :
                if self.holdom_master.isChecked() or self.holdom_vip.isChecked():
                    # 홀덤 클릭
                    print('Holdom 입장 중..')
                    Play_holdom(window,'holdom',self.holdom_master.isChecked(),self.holdom_vip.isChecked())

                    sleep(2)

                # 바카라 타이거6
                if self.tiger_master.isChecked() or self.tiger_vip.isChecked():
                    print('Baccarat Tiger 입장 중...')
                    Play_baccarat(window,'baccarat_tiger',self.tiger_master.isChecked(),self.tiger_vip.isChecked())

                    sleep(2)

                # 바카라 클래식
                if self.classic_master.isChecked() or self.classic_vip.isChecked():
                    print('Baccarat Classic 입장 중..')
                    Play_baccarat(window,'baccarat_classic',self.classic_master.isChecked(),self.classic_vip.isChecked())
                    
                    sleep(2)

                if self.blackjack_master.isChecked() or self.blackjack_vip.isChecked():
                    # Drag(window)

                    # # 바카라 블랙잭
                    # blackjack = Search_image_on_image(window,'blackjack.png',0.9)
                    # if blackjack is not None :
                    #     Click(blackjack)
            
                    # sleep(2)
                    pass

                # 바카라 파블로스
                if self.fabulos_master.isChecked() or self.fabulos_vip.isChecked():
                    Drag(window)

                    print('Baccarat Pabulos 입장 중...')
                    Play_baccarat(window,'baccarat_fabulos',self.fabulos_master.isChecked(),self.fabulos_vip.isChecked())

                    sleep(2)

    def Playing_thread(self,):
        thread = threading.Thread(target=self.Playing,args=(self,))
        thread.daemon=True
        thread.start()

    def button_click_event(self,):
        if not self.Start_or_Stop:
            self.Start_or_Stop = True
            self.start_Button.setText("STOP")

        else :
            self.Start_or_Stop = False
            self.start_Button.setText("START")


            

if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())