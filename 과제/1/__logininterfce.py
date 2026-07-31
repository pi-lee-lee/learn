
import sys
from ui.py import *
from core import *
from util import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial
from typing import Callable

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
            self.callback(self.ui.ID.text(), result)
            self.dialog.close()
            