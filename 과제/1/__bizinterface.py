import sys
from ui.py import *
from core import *
from util import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *



class BizInterface:
    def __init__(self,frame):
        self.bcore = Biz()
        self.ui = Ui_Biz()
        self.frame = frame
        self.id = ''

    def biz_run(self):
        self.set_biz_frame()
        self.show_product_view()

    def set_biz_frame(self):
        f = appendView(self.frame, self.ui)
        self.ui.ID.setText(self.id)       
        self.ui.ProductView.hide()
        self.ui.PartsView.hide()
        self.ui.OrderView.hide() 
        self.ui.NewView.hide()
        self.ui.RecipeView.hide()
        self.ui.ShowProduct.clicked.connect(self.show_product_view)
        self.ui.ShowParts.clicked.connect(self.show_parts_view)
        self.ui.ShowNew.hide()
        self.ui.ShowRecipe.hide()
        #self.ui.ShowNew.clicked.connect(self.show_new_view)
        #self.ui.ShowRecipe.clicked.connect(self.show_recipe_view)
        self.ui.ShowOrder.clicked.connect(self.show_orderlist_view)
        f.show()

    def set_table(self, tableview, labels, items, f_click ,hidden = False, hitem = 0, hpos = 1 ,single = False , f_select = None):
            if not items or len(items) < 1 :
                return
            model =  QStandardItemModel(len(items), len(labels))
            model.setHorizontalHeaderLabels(labels)
            self.tableview:QTableView = tableview
    
            self.tableview.setEditTriggers(QAbstractItemView.NoEditTriggers)   #편집불가
            self.tableview.setSelectionBehavior(QAbstractItemView.SelectRows)  #한줄선택
    
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

            if f_click != None:
                self.tableview.clicked.connect(lambda x : f_click(x))

            if f_select:
                self.tableview.selectionModel().selectionChanged.connect(lambda sel, dsel: f_select(sel, dsel))
            if single :
                self.tableview.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    
            return model

#####################################################################################################################################
    def show_product_view(self):
        if not self.ui.ProductView.isVisible():
            self.ui.ProductView.show()
            self.ui.PartsView.hide()
            self.ui.OrderView.hide()
            self.ui.NewView.hide()
            self.set_table_product_list()
            clearnView(self.ui.Side_Frame)

    def set_table_product_list(self):
        self.product_model = self.set_table(self.ui.ProductView, ['상품명','가격','제고','설명','상태'], self.bcore.get_product_list(), self.pruduct_item_click, True, 0, 1, True)
    
    def pruduct_item_click(self, index:QModelIndex):
        ppk = index.model().item(index.row(),0).data(Qt.ItemDataRole.UserRole)    
        self.set_product_side(ppk)
        self.selectedProductItem = index.row()

    def set_product_side(self, pk):
        pk = str(pk)
        self.up = Ui_ProductSide()
        changeView(self.ui.Side_Frame, self.up).show()
        product = self.bcore.get_product_item(pk)

        self.up.product_name.setText(product[1])
        self.up.name=product[1]
        self.up.product_name.textChanged.connect(lambda: self.enable_button_edit())
        self.up.product_price.setText(str(product[2]))
        self.up.price=product[2]
        self.up.product_price.textChanged.connect(lambda: self.enable_button_edit())
        self.up.product_des.setPlainText(product[4])
        self.up.product_des.textChanged.connect(lambda: self.enable_button_edit())
        self.up.des=product[4]
        self.up.product_inventory_count.setValue(int(product[3]))
        self.up.product_inventory_count.valueChanged.connect(lambda: self.enable_button_edit())
        self.up.inventory=int(product[3])
        self.up.product_state.setText('판매중' if product[5] == 'PS002' else '판매중지')
        self.up.product_state_checkbox.setChecked(True if product[5] == 'PS002' else False)
        self.up.product_state_checkbox.stateChanged.connect(lambda state: self.product_state_changed(state))
        self.up.state=product[5]

        self.up.button_delete.clicked.connect(lambda : self.delete_product(pk))
        self.up.button_edit.clicked.connect(lambda : self.edit_product(pk))
        self.up.button_edit.setEnabled(False)

        # self.up.product_inventory_count.valueChanged.connect(lambda x : self.set_product_side(pk))

    def enable_button_edit(self):
        if self.up.name == self.up.product_name.text() and \
           self.up.price == self.up.product_price.text() and \
           self.up.des == self.up.product_des.toPlainText() and \
           self.up.inventory == self.up.product_inventory_count.value() and \
           self.up.state == ('PS002' if self.up.product_state_checkbox.isChecked() else 'PS003'):
            self.up.button_edit.setEnabled(False)
        else:   
            self.up.button_edit.setEnabled(True)

    def delete_product(self, pk):
        self.bcore.delete_product(pk)
        self.set_table_product_list()
        clearnView(self.ui.Side_Frame)

    def edit_product(self, pk):
        name = self.up.product_name.text()
        price = self.up.product_price.text()
        des = self.up.product_des.toPlainText()
        state = 'PS002' if self.up.product_state_checkbox.isChecked() else 'PS003'
        quantity = self.up.product_inventory_count.value()

        if quantity == self.up.inventory:
            self.bcore.update_product(pk, name, price, des, state)
        else:
            self.bcore.update_product(pk, name, price, des, state, quantity)

        self.up.button_edit.setEnabled(False)
        self.set_table_product_list()

    def product_state_changed(self, state):
        self.up.product_state.setText('판매중' if state == Qt.Checked else '판매중지')
        self.enable_button_edit()

#####################################################################################################################################

    def show_parts_view(self):
        if not self.ui.PartsView.isVisible():
            self.ui.ProductView.hide()
            self.ui.PartsView.show()
            self.ui.OrderView.hide()
            self.ui.NewView.hide()
            self.set_table_parts_list()
            clearnView(self.ui.Side_Frame)

    def set_table_parts_list(self):
        self.parts_model = self.set_table(self.ui.PartsView, ['부품명','가격','제고'], self.bcore.get_parts_list(), self.parts_item_click, True, 0, 1, True)

    def parts_item_click(self, index:QModelIndex):
        ppk = index.model().item(index.row(),0).data(Qt.ItemDataRole.UserRole)    
        self.set_parts_side(ppk)
        self.selectedPartsItem = index.row()

    def set_parts_side(self, pk):
        pk = str(pk)
        self.ups = Ui_PartsSide()
        changeView(self.ui.Side_Frame, self.ups).show()
        parts = self.bcore.get_parts_item(pk)

        self.ups.part_name.setText(parts[1])
        self.ups.name=parts[1]
        self.ups.part_name.textChanged.connect(lambda: self.enable_button_edit_parts())
        self.ups.part_price.setText(str(parts[2]))
        self.ups.price=parts[2]
        self.ups.part_price.textChanged.connect(lambda: self.enable_button_edit_parts())
        self.ups.part_inventory_count.setValue(int(parts[3]))
        self.ups.part_inventory_count.valueChanged.connect(lambda: self.enable_button_edit_parts())
        self.ups.inventory=int(parts[3])

        self.ups.button_edit.clicked.connect(lambda : self.edit_parts(pk))
        self.ups.button_edit.setEnabled(False)

    def enable_button_edit_parts(self):
        if self.ups.name == self.ups.part_name.text() and \
           self.ups.price == self.ups.part_price.text() and \
           self.ups.inventory == self.ups.part_inventory_count.value():
            self.ups.button_edit.setEnabled(False)
        else:   
            self.ups.button_edit.setEnabled(True)   

    def edit_parts(self, pk):
        name = self.ups.part_name.text()
        price = self.ups.part_price.text()
        quantity = self.ups.part_inventory_count.value()

        self.bcore.update_parts(pk, name, price, quantity)

        self.ups.button_edit.setEnabled(False)
        self.set_table_parts_list()

#####################################################################################################################################

    def show_orderlist_view(self):
        if not self.ui.OrderView.isVisible():
            self.ui.ProductView.hide()
            self.ui.PartsView.hide()
            self.ui.OrderView.hide()
            self.ui.NewView.hide()
            self.ui.OrderView.show()
            self.set_table_order_list()
            clearnView(self.ui.Side_Frame)

    def set_table_order_list(self):
        self.order_model = self.set_table(self.ui.OrderView, 
                                          ['주문명', '상태', '주문일', '완료일'], 
                                          self.bcore.get_order_list(), 
                                          self.order_item_click, True, 0, 1, True)
        
    def order_item_click(self, index:QModelIndex):
        ppk = index.model().item(index.row(),0).data(Qt.ItemDataRole.UserRole)    
        self.set_order_side(ppk)
        self.selectedOrderItem = index.row()

    def set_order_side(self, pk):
        pk = str(pk)
        self.ol = Ui_OrderListSide()
        changeView(self.ui.Side_Frame, self.ol).show()
        self.set_table_order_items(pk)

        self.ol.order_cancle.clicked.connect(self.cancle_order)
        self.ol.order_receipt.clicked.connect(self.receipt_order)

    def set_table_order_items(self, order_id):
        parts = self.bcore.getOrderItems(order_id)
        self.order_item_model = self.set_table(
            self.ol.order_items,
            ['품명', '단가', '수량', '금액'],
            parts,None,
            True, 0, 1,
            single = True)

        total = sum(int(i[4]) for i in parts) if parts else 0    
        self.ol.sum_price.setText(str(total))

        if not self.order_item_model:
            return
    
        self.ol.order_items.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.ol.order_items.verticalHeader().hide()
        # self.ol.order_items.resizeColumnsToContents()


    def cancle_order(self):
        order_id = self.order_model.item(self.selectedOrderItem, 0).data(Qt.ItemDataRole.UserRole)
        self.bcore.cancle_order(order_id)
        self.set_table_order_list();

    def receipt_order(self):
        order_id = self.order_model.item(self.selectedOrderItem, 0).data(Qt.ItemDataRole.UserRole)
        try:
            self.bcore.receipt_order(order_id)
        except Exception as exp:
            if '부족합니다.' in str(exp):
                QMessageBox.information(self.frame,"재고부족",str(exp))
            else:
                raise exp
            
        self.set_table_order_list();
