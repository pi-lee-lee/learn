
from PyQt5 import QtWidgets
import sys
from ui.py import *


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

# MainWindow.findChild(QtWidgets.QWidget, 'Info').hid
# appendView(MainWindow.findChild(QtWidgets.QFrame, 'MainFrame'), Ui_User())

sys.exit(app.exec_())