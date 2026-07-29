import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("엑셀 스타일 테이블")
        self.resize(600, 300)

        # 1. 테이블 위젯 생성 (행 3개, 열 3개)
        self.table = QTableWidget(3, 3, self)
        self.setCentralWidget(self.table)

        # 2. 열 헤더(Header) 제목 설정
        self.table.setHorizontalHeaderLabels(["이름", "나이", "직업"])

        # 3. 데이터 넣기 (행 인덱스, 열 인덱스, QTableWidgetItem 객체)
        self.table.setItem(0, 0, QTableWidgetItem("김철수"))
        self.table.setItem(0, 1, QTableWidgetItem("25"))
        self.table.setItem(0, 2, QTableWidgetItem("개발자"))

        self.table.setItem(1, 0, QTableWidgetItem("이영희"))
        self.table.setItem(1, 1, QTableWidgetItem("30"))
        self.table.setItem(1, 2, QTableWidgetItem("디자이너"))

        self.table.setItem(2, 0, QTableWidgetItem("박민수"))
        self.table.setItem(2, 1, QTableWidgetItem("28"))
        self.table.setItem(2, 2, QTableWidgetItem("기획자"))



        self.model = QStandardItemModel(3, 3)
        
        # 3. 열 헤더 제목 설정
        self.model.setHorizontalHeaderLabels(["제품명", "수량", "가격"])

        # 4. 모델에 데이터 넣기 (행, 열, QStandardItem)
        self.model.setItem(0, 0, QStandardItem("노트북"))
        self.model.setItem(0, 1, QStandardItem("5"))
        self.model.setItem(0, 2, QStandardItem("1,200,000"))

        self.model.setItem(1, 0, QStandardItem("모니터"))
        self.model.setItem(1, 1, QStandardItem("10"))
        self.model.setItem(1, 2, QStandardItem("350,000"))

        self.model.setItem(2, 0, QStandardItem("마우스"))
        self.model.setItem(2, 1, QStandardItem("30"))
        self.model.setItem(2, 2, QStandardItem("45,000"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())