number = input("정수입력:")

if int(number) > 0 : 
    print("양수")

if int(number) < 0 : 
    print("음수")


if number[-1] in "02468" :
    print("str 짝수")
if number[-1] in "13579" :
    print("str 홀수 ")

if number[-1] in "02" :
    print("str2 짝수")
elif number[-1] in "468":
    print("str2 짝수2")
else :
    print("str2 홀수")




if int(number)%2 == 0 : 
    print("짝수")

if int(number)%2 == 1 : 
    print("홀수")

if int(number)%2 == 0 : 
    print("짝수")
else : 
    print("홀수")

import datetime

now = datetime.datetime.now()

print(now)

print(f"now.year = {now.year}년")
print(f"now.month = {now.month}월")
print(f"now.day = {now.day}일")
print(f"now.hour = {now.hour}시")
print(f"now.minute = {now.minute}분")
print(f"now.second = {now.second}초")
print(f"now.microsecond = {now.microsecond} 마이크로초")


if 0:
    print("0")
else:
    print("00")

if "": 
    print("0")
else:
    print("00")

if None: 
    print("0")
else:
    print("00")

if {}: 
    print("0")
else:
    print("00")


if number in "1":
    pass
else:
    pass

if number in "1":
    pass
else :
    raise NotImplementedError

# 문제 

