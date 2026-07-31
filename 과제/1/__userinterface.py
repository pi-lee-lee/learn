import sys
from ui.py import *
from core import *
from util import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class UserInterface:
    def __init__(self,frame):
        self.ucore = User()
        self.ui = Ui_User()
        self.frame = frame
        self.id = ''
    def user_run(self):
        self.set_user_frame()
        self.show_product_view()

    def set_user_frame(self):
        f = appendView(self.frame, self.ui)
        self.ui.ID.setText(self.id)       
        self.ui.OrderView.hide()
        self.ui.CartView.hide()
        self.ui.ProductView.hide() 
        self.ui.ShowProduct.clicked.connect(self.show_product_view)
        self.ui.ShowCart.clicked.connect(self.show_cart_view)
        self.ui.ShowOrder.clicked.connect(self.show_orderlist_view)
        f.show()


    def set_table(self, tableview, labels, items, func, hidden = False, hitem = 0, hpos = 1):
        if not items or len(items) < 1 :
            return
        model =  QStandardItemModel(len(items), len(labels))
        model.setHorizontalHeaderLabels(labels)
        self.tableview:QTableView = tableview
        self.tableview.setSelectionBehavior(QAbstractItemView.SelectRows)
        hidden_key = None;
        for i in range(len(items)):
            for j in range(len(items[i])) :
                if hidden:
                    if j == hitem:
                        hidden_key = items[i][j]
                        continue
                    elif j== hpos:
                        if not hidden_key:
                            raise Exception('제품 pk 날라감')
                        result = str(items[i][j]) 
                        item = QStandardItem(result)
                        item.setData(hidden_key, Qt.ItemDataRole.UserRole)
                        model.setItem(i,j-1,item)
                        hidden_key = None;
                    else :
                        result = str(items[i][j])
                        item = QStandardItem(result)
                        model.setItem(i,j-1,QStandardItem(result))
                else:
                    result = str(items[i][j])
                    item = QStandardItem(result)
                    model.setItem(i,j-1,QStandardItem(result))

        self.tableview.setModel(model)
        self.tableview.setStyleSheet("""
            /* 포커스가 있을 때와 없을 때 모두 선택된 셀의 배경색과 글자색을 고정 */
            QTableView::item:selected:active {
                background-color: #308CC6;  /* 원하는 선택 배경색 (예: 파란색) */
                color: white;               /* 글자색 */
            }
            QTableView::item:selected:!active {
                background-color: #308CC6;  /* 포커스가 빠져도 동일한 배경색 유지 */
                color: white;               /* 동일한 글자색 유지 */
            }
        """)
        self.tableview.clicked.connect(func)

        return model

#############################################################################
    def set_table_product_list(self):
        self.product_model = self.set_table(self.ui.ProductView, ['상품명','가격','설명'], self.ucore.getProductList(), self.pruduct_item_click, True, 0, 1)

    def set_order_side(self, pk, name, price, des = None):
        pk = str(pk)
        uo = Ui_OrderSide()
        changeView(self.ui.Side_Frame, uo).show()        
        order_sideView = changeView(self.ui.Side_Frame, uo)
        uo.ProductName.setText(name)
        uo.Price.setText(price)
        uo.CountBox.valueChanged.connect(lambda value : uo.Sum_Price.setText(f'{int(price)*value}'))
        uo.Sum_Price.setText(f'{price}')
        wc = uo.CountBox
        wc.setValue(1)
        uo.Order.clicked.connect(lambda: self.order_click(pk, wc.value()))
        uo.Cart.clicked.connect(lambda: self.cart_click(pk, wc.value()))
        order_sideView.show()

    def order_click(self, pk, count):
        self.ucore.sendOrder(self.id,pk,count)    

    def cart_click(self, pk, count):
        pk = self.product_model.item(self.selectedProductItem,0).data(Qt.ItemDataRole.UserRole)
        price = self.product_model.item(self.selectedProductItem,1).text()
        name = self.product_model.item(self.selectedProductItem,0).text()
        self.ucore.addCart(pk,name, price, count)    

    def pruduct_item_click(self, index:QModelIndex):
        ppk = index.model().item(index.row(),0).data(Qt.ItemDataRole.UserRole)
        pname = index.model().item(index.row(),0).text()
        price = index.model().item(index.row(),1).text()
        des = index.model().item(index.row(),2).text()        
        self.set_order_side(ppk, pname, price, des)
        self.selectedProductItem = index.row()


    def show_product_view(self):
        self.ui.ProductView.show()
        self.ui.CartView.hide()
        self.ui.OrderView.hide()
        self.set_table_product_list()
        clearnView(self.ui.Side_Frame)
        
##################################################################################
    def show_cart_view(self):
        self.ui.ProductView.hide()
        self.ui.CartView.hide()
        self.ui.OrderView.hide()
        # self.cart_model = self.set_table(self.ui.CartView, ['품명', '가격', '수량'], self.ucore.getCartList(), self.cart_item_click, True, 0, 1)
        clearnView(self.ui.Side_Frame)
        self.selectCartItem = None
        self.itemcount = None
        self.set_cart_side()
        
    def cart_item_click(self, index:QModelIndex):
        self.selectedCartItem = index.row()
        # self.set_order_side(ppk, pname, price)

    def set_cart_side(self):
        uc = Ui_CartSide()
        changeView(self.ui.Side_Frame, uc).show()
        self.cart_model = self.set_table(uc.CartView, ['품명', '가격', '수량'], self.ucore.getCartList(), self.cart_item_click, True, 0, 1)
        self.itemcount = uc.itemcount
        uc.itemcount.setText(str(self.ucore.getCartItemCount()))
        uc.delete_item.clicked.connect(self.cart_item_delete_click)
        uc.selected_item_count.valueChanged.connect(lambda value : self.cart_item_count_change(value))
        uc.order.clicked.connect(self.cart_order)
        
    def cart_item_delete_click(self):
        pk = self.cart_model.item(self.selectedCartItem,0).data(Qt.ItemDataRole.UserRole)
        self.ucore.removeCart(pk)
        self.cart_model.removeRow(self.selectedCartItem)
        self.itemcount.setText(str(self.ucore.getCartItemCount()))

    def cart_item_count_change(self,value):
        pk = self.cart_model.item(self.selectedCartItem,0).data(Qt.ItemDataRole.UserRole)
        self.cart_model.item(self.selectedCartItem,2).setText(str(value))
        self.ucore.editCart(pk,value)      

    def cart_order(self):

        pass


##################################################################################

    def show_orderlist_view(self):
        self.ui.ProductView.hide()
        self.ui.CartView.hide()
        self.ui.OrderView.show()


        clearnView(self.ui.Side_Frame)
        

    def set_orderlist_side(self):
        changeView(self.ui.Side_Frame, Ui_OrderListSide()).show()        










# 구 코드 혹시나 해서 일단 냅둠 

    # def set_table_product_list(self):    
            # results = User().getProductList()
            # cullist = ['상품명','가격','설명']
            # model =  QStandardItemModel(len(results), len(cullist))
            # model.setHorizontalHeaderLabels(cullist)
            
            # self.tableview:QTableView = self.ui.ProductView
            # self.tableview.setSelectionBehavior(QAbstractItemView.SelectRows)
            # product_key = None;
            # for i in range(len(results)):
            #     for j in range(len(results[i])) :
            #         if j == 0:
            #             product_key = results[i][j]
            #             continue
            #         elif j== 1:
            #             if not product_key:
            #                 raise Exception('제품 pk 날라감')
            #             result = str(results[i][j]) 
            #             item = QStandardItem(result)
            #             item.setData(product_key, Qt.ItemDataRole.UserRole)
            #             model.setItem(i,j-1,item)
            #             product_key = None;
            #         else :
            #             result = str(results[i][j])
            #             item = QStandardItem(result)
            #             model.setItem(i,j-1,QStandardItem(result))
            # self.tableview.setModel(model)
            # self.tableview.clicked.connect(self.pruduct_click)