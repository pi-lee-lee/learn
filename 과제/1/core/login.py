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
        result = con.execute("select u.CODEID, c.UPPER_CODE from User u, CODE c where u.ID = '{}' and u.PASS = {} and u.CODEID = c.CODEID".format(id,password)).fetchone()
        if result:
            print(result)
            return result

        return None