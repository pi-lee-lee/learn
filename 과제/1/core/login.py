from core.base import Base
from util.ConPool import TCon 

class Login(Base):

    def __init__(self):
        super().__init__();
        
    def check_id(self,id) -> bool:
        return True
    def check_password(self, password) -> bool:
        return True

    # def login(self, id, password):
    #     if self.check_password(password) and self.check_id(id): 
    #         con = self.dbm.get_connection()
    #         result = con.execute("select u.CODEID, c.UPPER_CODE from User u, CODE c where u.ID = '{}' and u.PASS = {} and u.CODEID = c.CODEID".format(id,password)).fetchone()
    #         if result:
    #             print(result)
    #             return result

    #     return None

    def login(self, id, password):
        if not self.check_id(id) or not self.check_password(password):
            return None

        con = self.dbm.get_connection()
        try:
            query = """select c.CODE, c.UPPER_CODE 
			from User u , CODE c  
           	where u.ID = '{}' and u.PASS = '{}' and u.CODEID  = c.CODEID ;
            """.format(id, password)
            return con.execute(query).fetchone()
        except Exception as exp:
            raise exp
            return None
        finally:
            con.close()