#문제 
import datetime

temp = input("입력:")

if "안녕" in temp :
    print("안녕하세요")

elif "몇 시" in temp or "몇시" in temp:
    now = datetime.datetime.now()
    print(f"지금 {now.hour}시입니다.")




number = input("정수를 입력 : ")

if int(number) % 5 == 0 :
    print(f"{number}은 5로 나누어 떨어지는 숫자입니다.")
else :
    print(f"{number}은 5로 나누어 떨어지지 않는 숫자입니다.")


if int(number) % 4 == 0 :
    print(f"{number}은 4로 나누어 떨어지는 숫자입니다.")
else :
    print(f"{number}은 4로 나누어 떨어지지 않는 숫자입니다.")

if int(number) % 3 == 0 :
    print(f"{number}은 3로 나누어 떨어지는 숫자입니다.")
else :
    print(f"{number}은 3로 나누어 떨어지지 않는 숫자입니다.")

if int(number) % 2 == 0 :
    print(f"{number}은 2로 나누어 떨어지는 숫자입니다.")
else :
    print(f"{number}은 2로 나누어 떨어지지 않는 숫자입니다.")


