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
        print(pk, count)

    def getOrderList(self):
        pass


