from util import DBmng
from sql_metadata import Parser
from typing import Tuple, List, Any

class Base:
    def __init__(self):
        self.dbm = DBmng() 
        
    # def select(self, con, query) ->  Tuple[List[str], List[Any]]:
    #     try:                
    #         results = con.execute(query)
    #         results = results.fetchall() 
    #         qparse = Parser(query)
    #         if qparse.output_columns[0] == '*':
    #             query = "SELECT column_name FROM information_schema.COLUMNS WHERE table_schema = DATABASE() AND table_name = '{}'  ORDER BY ordinal_position;".format(qparse.tables[0])
    #             cullist = [x[0] for x in con.execute(query).fetchall()]
    #         else :
    #             cullist = qparse.output_columns

    #         return (cullist, results)
    #     except Exception as exp:
    #         self.exp_print(exp)
        
    # def update(self, con, query):
    #     try:
    #         results = con.execute(query).rowcount       
    #         return results                  
    #     except Exception as exp:
    #         self.exp_print(exp)

    # def insert(self, con, query):
    #     try:
    #         results = con.execute(query).rowcount
    #         #results = results.lastrowid
    #         # results = results.rowcount
    #         # qparse = Parser(query)
    #         # query = "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_schema = DATABASE() AND table_name = '{}' and COLUMN_KEY ='pri' ORDER BY ordinal_position;".format(qparse.tables[0])
    #         # pri = con.execute(query).fetchone()[0]
    #         # query = "select * from {} where {}='{}'".format(qparse.tables[0], pri, results)
    #         # qparse = Parser(query)
    #         # self.select(con, query,qparse)
    #         return results
    #     except Exception as exp:
    #         self.exp_print(exp)
        
    # def delete(self, con, query):
    #     try:
    #         results = con.execute(query).rowcount
    #         # results = results.lastrowid
    #         # query = "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_schema = DATABASE() AND table_name = '{}' and COLUMN_KEY ='pri' ORDER BY ordinal_position;".format(qparse.tables[0])
    #         # pri = con.execute(query).fetchone()[0]
    #         # self.ui.textBrowser.setText(f"{pri} = '{results}'' 가 삭제되었습니다.")
    #         # self.ui.textBrowser.show()
    #         return results                        
    #     except Exception as exp:
    #         self.exp_print(exp)