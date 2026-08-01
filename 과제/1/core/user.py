from core.base import Base

class User(Base):
    def __init__(self):
        super().__init__();
        self.cart = {}

#############################################################################################
    def getCartList(self):
        if len(self.cart) > 0:
            results = self.getProductListInPid(self.cart.keys())
            for i in range(len(results)):
                if results[i][1] != self.cart[results[i][0]][0]:
                    self.cart[results[i][0]][0] = results[i][1]
                if results[i][2] != self.cart[results[i][0]][1]:
                    self.cart[results[i][0]][1] = results[i][2]


            return [[k, *v] for k, v in self.cart.items()]

        return None
    def getCartItemCount(self):
        return len(self.cart)

    def addCart(self, pk, name, price, count):
        self.cart[pk] = [name, price, count]

    def reset(self):
        self.cart = {}  
        
    def removeCart(self, pk):
        del self.cart[pk]

    def getcartsum(self):
        sum = 0
        for j in self.cart:
            sum += int(self.cart[j][1]) * int(self.cart[j][2])
        return sum

    def editCart(self, pk, count, name = None, price = None):
        if name :
            self.cart[pk][0] = name
        if price : 
            self.cart[pk][1] = price
        self.cart[pk][2] = count

    def sendCartOrder(self,id):
        try:
            con = self.dbm.get_connection()
            query = "select CONCAT('{}',NOW(3)+0) as key2 from dual;".format(id)

            order_id = con.execute(query).fetchone()[0]

            order_name = ""
            if len(self.cart) > 1:
                order_name = self.cart[list(self.cart.keys())[0]][0] + " 외 " + str(len(self.cart) - 1) + "건"
            else:
                order_name = self.cart[list(self.cart.keys())[0]][0]

            query = "INSERT INTO OrderList (U_ID, STATE, ORDER_DATE, COMP_DATE, ORDER_ID, ORDER_NAME) VALUES ('{}', NULL, NOW(), NULL, '{}', '{}');".format(id,order_id, order_name)
            result = con.execute(query)
            
            if not result or result.rowcount != 1:
                raise Exception('디비오류')
            for pk in self.cart: 
                values = self.cart[pk]
                query = "INSERT INTO OrderItems (ORDER_ID, P_ID, COUNT) VALUES('{}','{}',{})".format(order_id,pk,values[2])
                result = con.execute(query)
                if not result or result.rowcount != 1:
                    raise Exception('디비오류')
            con.commit()
            
        except Exception as exp:
            raise exp
        finally:
            con.close()
#############################################################################################

    def getProductList(self) :
        try:
            con = self.dbm.get_connection()
            return con.execute('select PID, NAME, PRICE, DES from Product').fetchall()
        except Exception as exp:
            raise exp
        finally:
            con.close()

    def getProductListInPid(self,pid) :
        try:
            con = self.dbm.get_connection()
            instr = ','.join([f"'{i}'" for i in pid])
            query = f"select PID, NAME, PRICE from Product where PID in ({instr})"            
            return con.execute(query).fetchall()
        except Exception as exp:
            raise exp
        finally:
            con.close()


#############################################################################################
    def sendOrder(self,id, pk, count, name):
        try:
            con = self.dbm.get_connection()
            query = "select CONCAT('{}',NOW(3)+0) as key2 from dual;".format(id)

            order_id = con.execute(query).fetchone()[0]
            
            query = "INSERT INTO OrderList (U_ID, STATE, ORDER_DATE, COMP_DATE, ORDER_ID, ORDER_NAME) VALUES ('{}', NULL, NOW(), NULL, '{}', '{}');".format(id,order_id, name)
            result = con.execute(query)
            if result and result.rowcount == 1:        
                query = "INSERT INTO OrderItems (ORDER_ID, P_ID, COUNT) VALUES('{}','{}',{})".format(order_id,pk,count)
                result = con.execute(query)
                if result and result.rowcount == 1:
                    con.commit()
            
        except Exception as exp:
            raise exp
        finally:
            con.close()
        print(pk, count)

    def sendOrderCancel(self, order_id):
        try:
            con = self.dbm.get_connection()
            query = "UPDATE OrderList SET STATE = 'OS008' WHERE ORDER_ID = '{}';".format(order_id)
            result = con.execute(query)
            if result and result.rowcount == 1:
                con.commit()
        except Exception as exp:
            print(exp)
            raise exp
        finally:
            con.close()

    def sendOrderMultipleCancel(self, order_ids):
        try:
            con = self.dbm.get_connection()
            instr = ','.join([f"'{i}'" for i in order_ids]) # , 뒤에 텍스트 조립 그리고 for 문으로 '오다아이디' 형식으로 리턴함 결론 '오다아이디', '오다아이디', '오다아이디' 
            query = f"UPDATE OrderList SET STATE = 'OS008' WHERE ORDER_ID in ({instr}) and IFNULL(STATE,'') != 'OS008' and IFNULL(STATE,'') not in  (select CODEID from CODE where UPPER_CODE_ID = 'OS003' );"
            result = con.execute(query)
            if result and result.rowcount > 0:
                con.commit()
        except Exception as exp:
            raise exp
        finally:
            con.close()

    def getOrderList(self, id):
        try:
            con = self.dbm.get_connection()
            query = """ select o.ORDER_ID,
                            o.ORDER_NAME,
                            COALESCE(c.CODE_NAME, '미접수') as STATE,
                            o.ORDER_DATE,
                            COALESCE(DATE(o.COMP_DATE), '') as COMP_DATE
                        from OrderList o
                        left join CODE c on o.STATE = c.CODEID
                        where o.U_ID = '{}'
                        order by o.ORDER_DATE desc ;
                    """.format(id)
            return con.execute(query).fetchall()
        except Exception as exp:
            raise exp
        finally:
            con.close()


    def getOrderItems(self, order_id):
        try:
            con = self.dbm.get_connection()
            query = """ select oi.P_ID, p.NAME, p.PRICE, oi.COUNT, oi.COUNT * p.PRICE as total
                        from OrderItems oi, Product p
                        where oi.P_ID = p.PID and oi.ORDER_ID = '{}'
                        order by p.NAME ;
                    """.format(order_id)
            return con.execute(query).fetchall()
        except Exception as exp:
            raise exp
        finally:
            con.close()

    


