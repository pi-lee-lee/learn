from core.base import Base

class User(Base):
    def __init__(self):
        super().__init__();
        self.cart = {}
        
    def getCartDict(self):
        print(self.cart)
        return self.cart

    def addCart(self, pk, count):
        self.cart[pk] = count
        print(pk, count)

    def removeCart(self, pk):
        del self.cart[pk]
        self.cart.remove()
        

    def editCart(self, pk, count):
        self.cart[pk] += count
        

    def getProductList(self) :
        try:
            con = self.dbm.get_connection()
            return con.execute('select PID, NAME, PRICE, DES from Product').fetchall()
        except Exception as exp:
            raise exp
        finally:
            con.close()

    def sendOrder(self, pk, count):
        try:
            con = self.dbm.get_connection()
            #CURDATE()
            query = "INSERT INTO OrderList (U_ID, P_ID, COUNT, STATE, ORDER_DATE, COMP_DATE) VALUES ('{}', '{}', {}, 'O', NOW(), NULL);".format('ADMIN',pk,count)
            result = con.execute(query)
            if result and result.rowcount == 1:
                con.commit()
             
        except Exception as exp:
            raise exp
        finally:
            con.close()
        print(pk, count)

    def getOrderList(self):
        pass


