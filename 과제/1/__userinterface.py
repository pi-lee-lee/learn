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



    def set_table(self, tableview, labels, items, f_click ,hidden = False, hitem = 0, hpos = 1 ,single = False , f_select = None):
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
        self.tableview.clicked.connect(lambda x : f_click(x))
        if f_select:
            self.tableview.selectionModel().selectionChanged.connect(lambda sel, dsel: f_select(sel, dsel))
        if single :
            self.tableview.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        return model

#############################################################################
    def set_table_product_list(self):
        self.product_model = self.set_table(self.ui.ProductView, ['상품명','가격','설명'], self.ucore.getProductList(), self.pruduct_item_click, True, 0, 1, f_select = self.pruduct_item_selected)
    def set_product_side(self, pk, name, price, des = None, mselected = False):
        pk = str(pk)
        uo = Ui_OrderSide()
        changeView(self.ui.Side_Frame, uo).show()
        if mselected :
            uo.ProductName.hide()
            uo.Price.hide()
            uo.CountBox.hide()
            uo.Sum_Price.hide()
            uo.Order.hide()
            uo.Cart.clicked.connect(lambda: self.cart_click(None, None))
        else:
            uo.ProductName.setText(name)
            uo.Price.setText(price)
            uo.CountBox.valueChanged.connect(lambda value : uo.Sum_Price.setText(f'{int(price)*value}'))
            uo.Sum_Price.setText(f'{price}')
            wc = uo.CountBox
            wc.setValue(1)
            uo.Order.clicked.connect(lambda: self.product_order_click(pk, wc.value(), name))
            uo.Cart.clicked.connect(lambda: self.cart_click(pk, wc.value()))
        

    def product_order_click(self, pk, count, name):
        self.ucore.sendOrder(self.id,pk,count,name)    

    def cart_click(self, pk, count):
        for i in self.ui.ProductView.selectedIndexes():
            pk = self.product_model.item(i.row(),0).data(Qt.ItemDataRole.UserRole)
            price = self.product_model.item(i.row(),1).text()
            name = self.product_model.item(i.row(),0).text()
            if len(self.ui.ProductView.selectedIndexes())//3 > 1 :
                self.ucore.addCart(pk,name, price, 1)
            else :
                self.ucore.addCart(pk,name, price, count)
           
    def pruduct_item_click(self, index:QModelIndex):
        if len(self.ui.ProductView.selectedIndexes())//3 > 1 :
            self.set_product_side(None, None, None, None, True)
        else:
            ppk = index.model().item(index.row(),0).data(Qt.ItemDataRole.UserRole)
            pname = index.model().item(index.row(),0).text()
            price = index.model().item(index.row(),1).text()
            des = index.model().item(index.row(),2).text()        
            self.set_product_side(ppk, pname, price, des)
            self.selectedProductItem = index.row()

    def pruduct_item_selected(self, sel, dsel):
        if len(self.ui.ProductView.selectedIndexes())//3 > 1 : 
            self.set_product_side(None, None, None, None, True)


    def show_product_view(self):
        if not self.ui.ProductView.isVisible():
            self.ui.ProductView.show()
            self.ui.CartView.hide()
            self.ui.OrderView.hide()
            self.set_table_product_list()
            clearnView(self.ui.Side_Frame)
        
##################################################################################
    def show_cart_view(self):
        # self.ui.ProductView.hide()
        # self.ui.CartView.show()
        # self.ui.OrderView.hide()
        # 이건 전에 메인뷰에 장바구니 표시되던 방식 
        # self.cart_model = self.set_table(self.ui.CartView, ['품명', '가격', '수량'], self.ucore.getCartList(), self.cart_item_click, True, 0, 1)
        clearnView(self.ui.Side_Frame)
        self.selectedCartItem = None
        self.set_cart_side()

    def set_cart_side(self):
        self.uc = Ui_CartSide()
        changeView(self.ui.Side_Frame, self.uc).show()

        self.cart_model = self.set_table(self.uc.CartView, ['품명', '가격', '수량'], self.ucore.getCartList(), self.cart_item_click, True, 0, 1)
        self.uc.itemcount.setText(str(self.ucore.getCartItemCount()))
        self.uc.delete_item.clicked.connect(lambda: self.cart_item_delete_click())
        self.uc.selected_item_count.valueChanged.connect(lambda value : self.cart_item_count_change(value))
        self.uc.order.clicked.connect(lambda: self.cart_order())
        self.uc.cart_sum.setText(str(self.ucore.getcartsum()))
        
    def cart_item_click(self, index:QModelIndex):
        if len(self.uc.CartView.selectedIndexes())//3 > 1 :
            self.selectedCartItem = None
            self.uc.selected_item_count.setValue(0)
        else:
            self.selectedCartItem = index.row()
            count = int(self.cart_model.item(index.row(),2).text())
            self.uc.selected_item_count.setValue(count)

        
    def cart_item_delete_click(self):
         if len(self.uc.CartView.selectedIndexes())//3 > 1 :
            pk = []
            row = []
            for i in self.uc.CartView.selectedIndexes():
                pk.append(self.cart_model.item(i.row(),0).data(Qt.ItemDataRole.UserRole))
                row.append(i.row())

            pk = list(set(pk))
            for i in pk:
                self.ucore.removeCart(i)

            row = list(set(row))
            row.sort(reverse=True)
            for i in row:
                self.cart_model.removeRow(i)
                        
            self.uc.itemcount.setText(str(self.ucore.getCartItemCount()))
            self.uc.cart_sum.setText(str(self.ucore.getcartsum()))
         else:
            pk = self.cart_model.item(self.selectedCartItem,0).data(Qt.ItemDataRole.UserRole)
            self.ucore.removeCart(pk)
            self.cart_model.removeRow(self.selectedCartItem)
            self.uc.itemcount.setText(str(self.ucore.getCartItemCount()))
            self.uc.cart_sum.setText(str(self.ucore.getcartsum()))

    def cart_order(self):
        self.ucore.sendCartOrder(self.id)
        self.ucore.reset()
        self.selectedCartItem = None
        self.uc.selected_item_count.blockSignals(True)
        self.uc.selected_item_count.setValue(0)
        self.uc.selected_item_count.blockSignals(False)
        self.cart_model.removeRows(0, self.cart_model.rowCount())   
        self.uc.itemcount.setText('0')
        self.uc.cart_sum.setText('0')

    def cart_item_count_change(self, value):
        if self.selectedCartItem is None:
            return
        item = self.cart_model.item(self.selectedCartItem, 0)
        count_item = self.cart_model.item(self.selectedCartItem, 2)

        if item is None:
            self.selectedCartItem = None
            return

        pk = item.data(Qt.ItemDataRole.UserRole)
        count_item.setText(str(value))
        self.ucore.editCart(pk, value)
        self.uc.cart_sum.setText(str(self.ucore.getcartsum()))


##################################################################################

        
    def show_orderlist_view(self):
        self.ui.ProductView.hide()
        self.ui.CartView.hide()
        self.ui.OrderView.show()
        clearnView(self.ui.Side_Frame)
        self.selectedOrderItem = None
        self.set_table_order_list()

    def set_table_order_list(self):
        self.orderlist_model = self.set_table(
            self.ui.OrderView,
            ['주문명', '상태', '주문일', '완료일'],     
            self.ucore.getOrderList(self.id),
            self.orderlist_item_click,
            True, 0, 1,
            f_select = self.orderlist_item_selected)

    def orderlist_selected_count(self):
        # 장바구니의 //3 하드코딩 대신 모델 컬럼 수로 계산
        if not self.orderlist_model:
            return 0
        return len(self.ui.OrderView.selectedIndexes()) // self.orderlist_model.columnCount()

    def orderlist_item_click(self, index:QModelIndex):
        if self.orderlist_selected_count() > 1:
            self.selectedOrderItem = None
            self.set_orderlist_side(None, True)
        else:
            self.selectedOrderItem = index.row()
            order_id = self.orderlist_model.item(index.row(), 0).data(Qt.ItemDataRole.UserRole)
            self.set_orderlist_side(order_id)              

    def orderlist_item_selected(self, sel, dsel):
        if self.orderlist_selected_count() > 1:
            self.selectedOrderItem = None
            self.set_orderlist_side(None, True)

    def set_orderlist_side(self, order_id, mselected = False):     
        self.ol = Ui_OrderListSide()
        changeView(self.ui.Side_Frame, self.ol).show()

        if mselected:
            self.ol.label_2.hide()
            self.ol.label_3.hide()
            self.ol.label_8.hide()
            self.ol.label_10.hide()
            self.ol.label_11.hide()
            self.ol.label_12.hide()
            self.ol.label_13.hide()
            self.ol.order_items.hide()
        else:
            self.ol.label_3.setText(str(order_id))
            self.set_table_order_items(order_id)            

        self.ol.order_cancle.clicked.connect(lambda: self.order_cancel_click())

    def set_table_order_items(self, order_id):
        items = self.ucore.getOrderItems(order_id)          
        self.orderitem_model = self.set_table(
            self.ol.order_items,
            ['품명', '단가', '수량', '금액'],
            items,
            lambda index: None,
            True, 0, 1,
            single = True)

        total = sum(int(i[4]) for i in items) if items else 0    
        self.ol.label_13.setText(str(total))

        if not self.orderitem_model:
            return
        self.ol.order_items.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ol.order_items.verticalHeader().hide()
        self.ol.order_items.resizeColumnsToContents()

    def order_cancel_click(self):
        if self.orderlist_selected_count() > 1:
            rows = list(set(i.row() for i in self.ui.OrderView.selectedIndexes()))
            order_ids = list(set(self.orderlist_model.item(r, 0).data(Qt.ItemDataRole.UserRole)
                                 for r in rows))
            self.ucore.sendOrderMultipleCancel(order_ids)
        elif self.selectedOrderItem is not None:
            rows = [self.selectedOrderItem]
            order_id = self.orderlist_model.item(self.selectedOrderItem, 0).data(Qt.ItemDataRole.UserRole)
            self.ucore.sendOrderCancel(order_id)
        else:
            return

        for r in rows:                                    
            self.orderlist_model.item(r, 1).setText('주문 취소')

        self.selectedOrderItem = None
        clearnView(self.ui.Side_Frame)