
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from __userinterface import UserInterface
from __bizinterface import BizInterface
from ui.py import *
from core import *
from util import *
from typing import Callable

class MainInterface:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.id = None
        self.uu = None
        self.bi = None
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
        self.ui.BizMode.clicked.connect(self.run_biz_mode)

    def hideInfo(self):
        self.MainWindow.findChild(QWidget, 'Info').hide()

    def click_login(self):
        if self.ui.Login.text() == "로그인":
            self.show_login_dialog()
        else:
            self.ui.Info.show()
            for i in self.ui.MainFrame.findChildren(QFrame):
                i.setParent(None)
            self.id = None
            self.uu = None
            self.ui.AdminFrame.hide()
            self.ui.Login.setText('로그인')

    def show_login_dialog(self):
        li = LoginInterface(self.MainWindow)
        li.show_login(self.callback_login)

    def callback_login(self, id, code, upper_code):
        self.ui.AdminFrame.hide()
        if code == 'AUTH_ADMIN':
            self.id = id
            self.ui.AdminFrame.show()

        if upper_code == 'AUTH_PARTNER':
            self.ui.AdminFrame.hide()
            self.id = id
            self.run_biz_mode()

        if upper_code == 'AUTH_USER':
            self.ui.AdminFrame.hide()
            self.id = id
            self.run_user_mode()

        self.ui.Login.setText('로그아웃')

    def run_user_mode(self):
        if self.id:
            self.hideInfo()
            clearnView(self.ui.MainFrame)
            self.uu = UserInterface(self.ui.MainFrame)
            self.uu.id = self.id
            self.uu.user_run()

    def run_biz_mode(self):
        if self.id:
            self.hideInfo()
            clearnView(self.ui.MainFrame)
            self.bi = BizInterface(self.ui.MainFrame)
            self.bi.id = self.id
            self.bi.biz_run()


class LoginInterface:
    def __init__(self,window):
        self.lcore = Login()
        self.ui = Ui_Login()
        self.window = window
                        
    def show_login(self, callback:Callable[[str,str],None]):
        self.dialog = QDialog(self.window)
        self.ui.setupUi(self.dialog)
        self.dialog.show()
        self.callback = callback
        self.init_connect()

    def init_connect(self):
        self.ui.Button_Login.clicked.connect(lambda: self.login(self.ui.ID.text(),self.ui.PASS.text()))

    def login(self,id,password):
        result = self.lcore.login(self.ui.ID.text(),self.ui.PASS.text())
        if not result:
            self.ui.INFO.setText('로그인실패 아직 준비가 안됐다.')
        else:
            self.callback(self.ui.ID.text(), result[0], result[1])
            self.dialog.close()