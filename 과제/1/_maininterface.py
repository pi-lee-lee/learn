
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from __userinterface import UserInterface
from __logininterfce import LoginInterface
from ui.py import *
from core import *
from util import *

class MainInterface:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.ui.AdminFrame.hide()
        self.init_connect()

    def main_run(self) -> QApplication:
        try:
            self.MainWindow.show()
            sys.exit(self.app.exec_())
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_lineno)
            print(e.__traceback__.tb_frame.f_code.co_filename)
        


    def init_connect(self):
        self.ui.Login.clicked.connect(self.click_login)
        self.ui.UserMode.clicked.connect(self.run_user_mode)

    def hideInfo(self):
        self.MainWindow.findChild(QWidget, 'Info').hide()

    def click_login(self):
        if self.ui.Login.text() == "로그인":
            self.show_login_dialog()
        else :
            self.ui.Info.show()
            for i  in self.ui.MainFrame.findChildren(QFrame):
                i.setParent(None)
            self.ui.Login.setText('로그인')

    def show_login_dialog(self):
        li = LoginInterface(self.MainWindow)
        li.show_login(self.callback_login)

    def callback_login(self, id, code, upper_code):
        self.id = id
        if code == 'AA001':
            print("관리자모드")
            self.ui.AdminFrame.show()
        elif upper_code == 'AU002':
            print('사업자모드')
        elif upper_code == 'AU003':
            self.run_user_mode()
            print('사용자모드')

        self.ui.Login.setText('로그아웃')

    def run_user_mode(self):
        self.hideInfo()
        self.uu = UserInterface(self.ui.MainFrame)
        self.uu.id = self.id
        self.uu.user_run()
