from core.base import Base
from util.ConPool import TCon 

class Login(Base):

    def __init__(self):
        super().__init__();
        
    def check_id(self,id) -> bool:
        return True
    def check_password(self, password) -> bool:
        return True

    def login(self, id, password):
        if (not self.check_password) or (not self.check_id): 
            return False

        con = self.dbm.get_connection()
        result = con.execute("select CODE from User where ID = '{}' and PASS = {}".format(id,password)).fetchone()
        if result:
            receiveCode = result[0]
            return receiveCode

        return None