from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from ui_design import Ui_Dialog
from sql_metadata import Parser
import sys
from datetime import date, datetime


from ConPool import DBmng, TCon



class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.dbpool = DBmng()
        self.list_init()
        self.ui.button_clear.clicked.connect(self.clear)
        self.ui.button_run.clicked.connect(self.run)
        self.ui.button_commit.clicked.connect(self.commit)
        self.ui.button_rollback.clicked.connect(self.rollback)
        self.ui.textBrowser.hide()
        self.con = None

    def select(self, con, query, qparse):
        try:
            results = con.execute(query)
            results = results.fetchall() 

            if qparse.output_columns[0] == '*':
                query = "SELECT column_name FROM information_schema.COLUMNS WHERE table_schema = DATABASE() AND table_name = '{}'  ORDER BY ordinal_position;".format(qparse.tables[0])
                cullist = [x[0] for x in con.execute(query).fetchall()]
            else :
                cullist = qparse.output_columns

            print(len(cullist), len(results))
            model =  QStandardItemModel(len(cullist), len(results))
            model.setHorizontalHeaderLabels(cullist)

            for i in range(len(results)):
                for j in range(len(results[i])) :

                    if isinstance(results[i][j], (date, datetime)):
                        result = results[i][j].strftime('%Y-%m-%d')  # 시/분/초까지 필요하면 '%Y-%m-%d %H:%M:%S'
                    else:
                        result = str(results[i][j]) # 숫자 등 다른 타입도 문자열로 안전하게 변환
                    # print(results[i][j])
                    model.setItem(i,j,QStandardItem(result))
            self.ui.tableView.setModel(model)
        except Exception as exp:
            log = f"{exp}\n오류라인 : {exp.__traceback__.tb_lineno}\n프레임정보:{exp.__traceback__.tb_frame}"
            self.ui.textBrowser.setText(log)
            self.ui.textBrowser.show()
            raise exp
        
    def update(self, con, query, qparse):
        pass

    def insert(self, con, query, qparse):
        try:
            results = con.execute(query)
            results = results.lastrowid
            query = "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_schema = DATABASE() AND table_name = '{}' and COLUMN_KEY ='pri' ORDER BY ordinal_position;".format(qparse.tables[0])
            pri = con.execute(query).fetchone()[0]
            query = "select * from {} where {}='{}'".format(qparse.tables[0], pri, results)
            qparse = Parser(query)
            self.select(con, query,qparse)
        except Exception as exp:
            log = f"{exp}\n오류라인 : {exp.__traceback__.tb_lineno}\n프레임정보:{exp.__traceback__.tb_frame}"
            self.ui.textBrowser.setText(log)
            self.ui.textBrowser.show()
            raise exp
        
    def delete(self, con, query, qparse):
        try:
            results = con.execute(query)
            results = results.lastrowid
            query = "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_schema = DATABASE() AND table_name = '{}' and COLUMN_KEY ='pri' ORDER BY ordinal_position;".format(qparse.tables[0])
            pri = con.execute(query).fetchone()[0]
            self.ui.textBrowser.setText(f"{pri} = '{results}'' 가 삭제되었습니다.")
            self.ui.textBrowser.show()                        
        except Exception as exp:
            log = f"{exp}\n오류라인 : {exp.__traceback__.tb_lineno}\n프레임정보:{exp.__traceback__.tb_frame}"
            self.ui.textBrowser.setText(log)
            self.ui.textBrowser.show()
            raise exp
                

    def run(self):
        self.ui.textBrowser.hide()
        query = self.ui.textEdit.toPlainText()

        qparse = Parser(query)
        type = qparse.query_type.upper()

        try:
            if self.con == None:
                con = self.dbpool.get_connection()
            else:
                con = self.con
            if type == 'SELECT':
                self.select(con,query,qparse)
            elif type == 'UPDATE':
                self.con = con
                self.update(con,query,qparse)
            elif type == 'DELETE':
                self.con = con
                self.delete(con,query,qparse)
            elif type == 'INSERT':
                self.con = con
                self.insert(con,query,qparse)
            else:
                self.ui.textBrowser.setText('DML 기본만 지원합니다. ')
                self.ui.textBrowser.show()   

        except Exception as exp:
            self.exp_print(exp)
        finally:
            if self.con == None:
                con.close()

    def exp_print(self,exp):
        log = f"{exp}\n오류라인 : {exp.__traceback__.tb_lineno}\n프레임정보:{exp.__traceback__.tb_frame}"
        self.ui.textBrowser.setText(log)
        self.ui.textBrowser.show()
        raise exp
                        
    def clear(self):
        self.ui.textEdit.setText('')

    def commit(self):
        if self.con:
            try :
                self.con.commit()
                self.list_init()
            except Exception as exp:
                self.exp_print(exp)
            finally:
                self.con.close()
                self.con = None
    def rollback(self):
        if self.con:
            try:   
                self.con.rollback()
            except Exception as exp:
                self.exp_print(exp)
            finally:
                self.con.close()
                self.con = None

    def list_init(self):
        con = self.dbpool.get_connection()
        try:
            result = con.execute( """
            SELECT 
                table_name AS '테이블명',
                table_rows AS '데이터 로우수'
    --            ROUND(((data_length + index_length) / 1024 / 1024), 2) AS '전체 용량(MB)',
    --            ROUND((data_length / 1024 / 1024), 2) AS '데이터 용량(MB)',
    --            ROUND((index_length / 1024 / 1024), 2) AS '인덱스 용량(MB)',
    --            create_time AS '생성일시'
            FROM 
                information_schema.TABLES
            WHERE 
                table_schema = DATABASE()  -- 현재 접속 중인 DB 기준
            ORDER BY 
                (data_length + index_length) DESC; -- 용량이 큰 순서대로 정렬 
            """)

            array = []

            for i in result.fetchall():
                array.append('{}({})'.format(i[0],i[1]))

            list = QStringListModel()
            list.setStringList(array)
            self.ui.listView.setModel(list)

        except Exception as exp:
            log = f"{exp}\n오류라인 : {exp.__traceback__.tb_lineno}\n프레임정보:{exp.__traceback__.tb_frame}"
            self.ui.textBrowser.setText(log)
            self.ui.textBrowser.show()
        finally:
            con.close()

            
if __name__ == '__main__':
    app = QApplication(sys.argv)

    my = Window()

    my.show()
    sys.exit(app.exec())

