MENU = {'계좌개설':    {'arg':['계좌번호'], 'func':1},
                     '계좌삭제':    {'arg':['계좌번호'], 'func':1}, 
                     '입금': {'arg':['계좌번호','금액'], 'func':1}, 
                     '출금': {'arg':['계좌번호','금액'], 'func':1}, 
                     '출력': {'arg':[], 'func':1}, 
                     '종료': {'arg':[], 'func':1}}

item = MENU['입금']

for i in MENU['입금']['arg']:
    print(i)






print(any([False,False,True]))