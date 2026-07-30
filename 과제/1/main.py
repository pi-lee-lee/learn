
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


import sys
from ui.py import *
from core import *
from util import *
from PyQt5.QtGui import *

product_key_list = []

uu = User()

def hideInfo():
    MainWindow.findChild(QWidget, 'Info').hide()

def order_click(pk, count):
    print(pk, count)
    print(type(pk), type(count))
    uu.sendOrder(pk,count)    

def cart_click(pk, count):
    print(pk, count)
    print(type(pk), type(count))
    uu.addCart(pk,count)    

def show_cart_side():
    changeView(MainWindow.findChild(QWidget, 'Side_Frame'), Ui_CartSide()).show()
    

def show_orderlist_side():
    changeView(MainWindow.findChild(QWidget, 'Side_Frame'), Ui_OrderListSide()).show()
    
      

def show_order_side(pk, name, price, des):
    pk = str(pk)
    order_sideView = changeView(MainWindow.findChild(QWidget, 'Side_Frame'), Ui_OrderSide())
    order_sideView.show()

    order_sideView.findChild(QWidget,'ProductName').setText(name)
    order_sideView.findChild(QWidget,'Price').setText(price)
    
    wp = order_sideView.findChild(QWidget,'Sum_Price')
    wp.setText(f'{price}')
    order_sideView.findChild(QWidget,'CountBox').valueChanged.connect(lambda value : wp.setText(f'{int(price)*value}'))

    wc = order_sideView.findChild(QWidget,'CountBox')
    wc.setValue(1)
    order_sideView.findChild(QWidget,'Order').clicked.connect(lambda: order_click(pk, wc.value()))

    order_sideView.findChild(QWidget,'Cart').clicked.connect(lambda: cart_click(pk, wc.value()))

def pruduct_click(index:QModelIndex):
    ppk = index.model().item(index.row(),0).data(Qt.ItemDataRole.UserRole)
    pname = index.model().item(index.row(),0).text()
    price = index.model().item(index.row(),1).text()
    des = index.model().item(index.row(),2).text()        
    show_order_side(ppk, pname, price, des)

def setProcuetList():
    results = User().getProductList()
    cullist = ['상품명','가격','설명']
    model =  QStandardItemModel(len(results), len(cullist))
    model.setHorizontalHeaderLabels(cullist)
    tableview:QTableView = MainWindow.findChild(QWidget, 'MainFrame').findChild(QWidget,'ProductView')
    tableview.setSelectionBehavior(QAbstractItemView.SelectRows)
    product_key = None;
    for i in range(len(results)):
        for j in range(len(results[i])) :
            if j == 0:
                product_key = results[i][j]
                continue
            elif j== 1:
                if not product_key:
                    raise Exception('제품 pk 날라감')
                result = str(results[i][j]) 
                item = QStandardItem(result)
                item.setData(product_key, Qt.ItemDataRole.UserRole)
                model.setItem(i,j-1,item)
                product_key = None;
            else :
                result = str(results[i][j])
                item = QStandardItem(result)
                model.setItem(i,j-1,QStandardItem(result))
    tableview.setModel(model)
    tableview.clicked.connect(pruduct_click)

def setUserFrame():
    appendView(MainWindow.findChild(QWidget, 'MainFrame'), Ui_User()).show()
    MainWindow.findChild(QWidget, 'MainFrame').findChild(QPushButton,'ShowCart').clicked.connect(show_cart_side)
    MainWindow.findChild(QWidget, 'MainFrame').findChild(QPushButton,'ShowOrder').clicked.connect(show_orderlist_side)
        
###################################################################################   
app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

print(Login().login('ADMIN','1234'))

hideInfo()

setUserFrame()

setProcuetList()

sys.exit(app.exec_())


