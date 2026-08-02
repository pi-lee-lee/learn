from core.base import Base

# 일단 나중에 이걸로 리턴 ㅡ.ㅡ; 지금 귀찮아. 
# class Product(Base):
#     def __init__(self, pid, name, price, state, quantity, des):
#         super().__init__();
#         self.pid = pid
#         self.name = name
#         self.price = price
#         self.state = state
#         self.quantity = quantity
#         self.des = des

# class Parts(Base):
#     def __init__(self, pid, name, price, state, quantity):
#         super().__init__();
#         self.pid = pid
#         self.name = name
#         self.price = price
#         self.state = state
#         self.quantity = quantity

class Biz(Base):
    def __init__(self):
        super().__init__();



################################################################################################################
    def get_product_list(self) :
        try:
            con = self.dbm.get_connection()
            return con.execute("""select p.PID, p.NAME, p.PRICE, i.QUANTITY, p.DES, 
                                      CASE p.STATE 
                                        WHEN 'PS002' THEN '판매중' 
                                        WHEN 'PS003' THEN '판매중지' 
                                        ELSE '알 수 없음' END as STATE 
                                  from Product p , Inventory i 
                                  where p.PID = i.I_ID
                                  and p.STATE != 'PS004'""").fetchall()
        except Exception as exp:
            raise exp
        finally:
            con.close()

    def get_product_item(self,pk) :
        try:
            con = self.dbm.get_connection()
            return con.execute(f"select p.PID, p.NAME, p.PRICE, i.QUANTITY, p.DES, p.STATE from Product p , Inventory i where p.PID = i.I_ID and p.PID = '{pk}'").fetchone()
        except Exception as exp:
            raise exp
        finally:
            con.close()

    def get_product_list_in_pid(self,pid) :
        try:
            con = self.dbm.get_connection()
            instr = ','.join([f"'{i}'" for i in pid])
            query = f"select PID, NAME, PRICE from Product where PID in ({instr})"            
            return con.execute(query).fetchall()
        except Exception as exp:
            raise exp
        finally:
            con.close()

    def update_product(self, pk, name, price, des, state, quantity = None) :
        try:
            con = self.dbm.get_connection()
            query = f"update Product set NAME = '{name}', PRICE = {price}, DES = '{des}', STATE = '{state}' where PID = '{pk}'"
            result = con.execute(query)
            if not result or result.rowcount != 1:
                raise Exception('디비오류')
            if quantity is not None:
                self.change_product_quantity(pk, quantity)

            con.commit()
        except Exception as exp:
            print(exp)
            raise exp
        finally:
            con.close()

    def delete_product(self, pk) :
        try:
            con = self.dbm.get_connection()
            query = f"update Product set STATE = 'PS004' where PID = '{pk}'"
            result = con.execute(query)
            if not result or result.rowcount != 1:
                raise Exception('디비오류')
            con.commit()
        except Exception as exp:
            print(exp)
            raise exp
        finally:
            con.close()
    

    def change_product_quantity(self, pk, quantity) :
        try:
            con = self.dbm.get_connection()
            query = f"""
                        select p.PPID, p.NAME, r.COUNT*{quantity} ,i.QUANTITY   
                        from Recipe r, Part p, Inventory i  
                        WHERE r.P_ID = '{pk}' and r.PP_ID = p.PPID and p.PPID  = i.I_ID 
                     """
            results = con.execute(query).fetchall()
            if not results or len(results) < 0:
                raise Exception('No Recipe Data not Change Product Quantity')
            
            checkstr = ''
            for result in results:
                if result[3] < result[2]:
                    checkstr += f'부품 재고가 부족합니다. {result[1]} : {result[3]} / {result[2]}\n'
                else:
                    if checkstr == '':
                        query = f"update Inventory set QUANTITY = QUANTITY - {result[2]} where I_ID = '{result[0]}'"
                        result = con.execute(query)
                        if not result or result.rowcount != 1:
                            raise Exception('디비오류')

            if checkstr != '':
                con.rollback()
                raise Exception(checkstr)

            query = f"update Inventory set QUANTITY = {quantity} where I_ID = '{pk}'"
            result = con.execute(query)
            if not result or result.rowcount != 1:
                raise Exception('디비오류')

            con.commit()
        except Exception as exp:
            print(exp)
            raise exp
        finally:
            con.close()

################################################################################################################

    def get_parts_list(self) :
        try:
            con = self.dbm.get_connection()
            return con.execute("""select p.PPID, p.NAME, p.PRICE, i.QUANTITY
                                  from Part p , Inventory i 
                                  where p.PPID = i.I_ID
                                  """).fetchall()
        except Exception as exp:
            raise exp
        finally:
            con.close()

    def get_parts_item(self,pk) :
        try:
            con = self.dbm.get_connection()
            return con.execute(f"select p.PPID, p.NAME, p.PRICE, i.QUANTITY from Part p , Inventory i where p.PPID = i.I_ID and p.PPID = '{pk}'").fetchone()
        except Exception as exp:
            raise exp
        finally:
            con.close()

    def update_parts(self, pk, name, price, quantity) :
        try:
            con = self.dbm.get_connection()
            query = f"update Part set NAME = '{name}', PRICE = {price} where PPID = '{pk}'"
            result = con.execute(query)
            if not result or result.rowcount != 1:
                raise Exception('디비오류')

            query = f"update Inventory set QUANTITY = {quantity} where I_ID = '{pk}'"
            result = con.execute(query)
            if not result or result.rowcount != 1:
                raise Exception('디비오류')

            con.commit()
        except Exception as exp:
            print(exp)
            raise exp
        finally:
            con.close()

################################################################################################################

    def get_order_list(self) :
        try:
            con = self.dbm.get_connection()
            query = """ select o.ORDER_ID,
                            o.ORDER_NAME,
                            COALESCE(c.CODE_NAME, '미접수') as STATE,
                            o.ORDER_DATE,
                            COALESCE(DATE(o.COMP_DATE), '') as COMP_DATE
                        from OrderList o
                        left join CODE c on o.STATE = c.CODEID
                        where COALESCE(o.STATE, ' ') != 'OS008'
                        order by o.STATE, o.ORDER_DATE desc  ;
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


    def cancle_order(self, order_id):
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

    def receipt_order(self, order_id):
        try:
            con = self.dbm.get_connection()
            query = f"""
                    select oi.P_ID, p.name, oi.COUNT, i.QUANTITY  
                    from Product p, OrderItems oi, OrderList ol, Inventory i 
                    where p.pid = oi.P_ID and  oi.ORDER_ID = ol.ORDER_ID and oi.P_ID = i.I_ID 
                    and ol.ORDER_ID = '{order_id}';
            """
            results = con.execute(query).fetchall()

            checkstr = ''
            for result in results:
                if result[3] < result[2]:
                    checkstr += f'제품 재고가 부족합니다. {result[1]} : {result[3]} / {result[2]}\n'
                else:
                    if checkstr == '':
                        query = f"update Inventory set QUANTITY = QUANTITY - {result[2]} where I_ID = '{result[0]}'"
                        result = con.execute(query)
                        if not result or result.rowcount != 1:
                            raise Exception('디비오류') 

            if checkstr != '':
                con.rollback()
                raise Exception(checkstr)
            
            query = "UPDATE OrderList SET STATE = 'OS004' WHERE ORDER_ID = '{}';".format(order_id)
            result = con.execute(query)
            if result and result.rowcount == 1:
                con.commit()
            
        except Exception as exp:
            print(exp)
            raise exp
        finally:
            con.close()
