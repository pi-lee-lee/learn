
class Bank(BaseException):
    def __init__(self):
        self.MENU = {'계좌개설':    {'arg':['계좌번호'], 'func':self.make},
                     '계좌삭제':    {'arg':['계좌번호'], 'func':self.delete}, 
                     '입금': {'arg':['계좌번호','금액'], 'func':self.add}, 
                     '출금': {'arg':['계좌번호','금액'], 'func':self.minus}, 
                     '출력': {'arg':[], 'func':self.print}, 
                     '종료': {'arg':[], 'func':self.exit}}
        self.dic = {'1':0}
        self.cmd = None
        self.state = None

    def inputNum(self, message, count=5):
        for i in range(count):
            num = input(f'{message}:' if i == 0 else f'{message}재입력')
            if not num.isdigit():
                print('숫자만 입력합니다.')
                continue
            return num
        return None

    def print_menu(self):
        count = 0
        for i in self.MENU.keys():
            count += 1
            print(f'{count} : {i}')

    def select_menu(self,cmd):        
        try:
            self.cmd = int(cmd)
        except BaseException as exp:
            print('숫자만 입력하세요')
            return
        
        if self.cmd > len(self.MENU):
            return None
        else:
            argv = []
            count = 0;
            for i in self.MENU[(list(self.MENU.keys())[self.cmd-1])]['arg']:
                count += 1
                temp = self.inputNum(i)
                if temp :
                    argv.append(temp)

            if count is len(argv):
                self.MENU[(list(self.MENU.keys())[self.cmd-1])]['func'](*argv)
            else:
                print('파라메터오류')

    def is_able_account(self,account):
        if account in self.dic:
            print('있는계좌')
            return True
        else :
            print('없는계좌')
            return False

    def make(self,*arg):
        if not self.is_able_account(arg[0]) :
            self.dic[arg[0]] = 0
            print('계좌개설됨 : ', arg[0])
        else :
            print('있는계좌')

    def delete(self,*arg):
        if self.is_able_account(arg[0]) : 
            del self.dic[arg[0]]
            print('계좌삭제')
        
    def add(self,*arg):
        if self.is_able_account(arg[0]) :
            self.dic[arg[0]] += int(arg[1])
            print('입금')
        
    def minus(self,*arg):
        if self.is_able_account(arg[0]) :
            self.dic[arg[0]] -= int(arg[1])
            print('출금')
        

    def print(self,*arg):
        for i,m in self.dic.items():
            print(f'{i} : {m}원')


    def exit(self):
        self.state = 'exit'

    def start(self):
        while self.state is not 'exit' :
            self.print_menu()
            self.select_menu(input('메뉴선택:'))

Bank().start()
