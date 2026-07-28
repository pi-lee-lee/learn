from db.ConPool import *
from Customer import Customer

db_manager = DBmng()
con = db_manager.get_connection()
result = con.execute('select * from Customers')

map = result.mappings()
cul = map.keys()
val = result.columns('Name')
print(val.fetchall())
cuslist = []




con.close()