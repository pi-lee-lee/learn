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
            # cartlist = []
            # for i in self.cart:
            #     cartlist.append([i,*self.cart[i]])
            # return cartlist
        return None
    def getCartItemCount(self):
        return len(self.cart)

    def addCart(self, pk, name, price, count):
        self.cart[pk] = [name, price, count]

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

            query = "INSERT INTO OrderList (U_ID, STATE, ORDER_DATE, COMP_DATE, ORDER_ID) VALUES ('{}', 'O', NOW(), NULL, '{}');".format(id,order_id)
            result = con.execute(query)
            
            if not result and result.rowcount != 1:
                raise Exception('디비오류')
            for pk in self.cart: 
                values = self.cart[pk]
                query = "INSERT INTO OrderItems (ORDER_ID, P_ID, COUNT) VALUES('{}','{}',{})".format(order_id,pk,values[2])
                con.execute(query)
                if not result and result.rowcount != 1:
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
    def sendOrder(self,id, pk, count):
        try:
            con = self.dbm.get_connection()
            query = "select CONCAT('{}',NOW(3)+0) as key2 from dual;".format(id)

            order_id = con.execute(query).fetchone()[0]

            query = "INSERT INTO OrderList (U_ID, STATE, ORDER_DATE, COMP_DATE, ORDER_ID) VALUES ('{}', 'O', NOW(), NULL, '{}');".format(id,order_id)
            result = con.execute(query)
            if result and result.rowcount == 1:        
                query = "INSERT INTO OrderItems (ORDER_ID, P_ID, COUNT) VALUES('{}','{}',{})".format(order_id,pk,count)
                results = con.execute(query)
                if result and result.rowcount == 1:
                    con.commit()
            
        except Exception as exp:
            raise exp
        finally:
            con.close()
        print(pk, count)

    def getOrderList(self):
        pass


