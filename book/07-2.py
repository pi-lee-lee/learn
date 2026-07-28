from urllib import request
from bs4 import BeautifulSoup 


target = request.urlopen('https://www.weather.go.kr/w/weather/land/city-obs.do')


soup = BeautifulSoup(target,'html.parser')

print(soup)

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hellow():
    return "helllow world"


from functools import wraps

def test(function):
    @wraps(function)
    def wrapper(*arg, **kwargs):
        print('start')
        function()
        print('end')
    return wrapper


@test
def hello(*arg):
    for i in arg:
        print(i)
    print('hello')

hello(1,2,3,4,5)

import functools

# 1. 원본 함수 속성을 유지해주는 '진짜' 데코레이터 정의
def my_decorator(func):
    @functools.wraps(func)  # <- 이 부분이 문서에서 설명한 편의 기능입니다.
    def wrapper(*args, **kwargs):
        print("💡 [전처리] 함수 실행 전")
        result = func(*args, **kwargs)
        print("💡 [후처리] 함수 실행 후")
        return result
    return wrapper

# 2. 데코레이터 적용
@my_decorator
def greet(name):
    """사용자에게 인사를 건네는 함수입니다."""
    print(f"안녕하세요, {name}님!")

# 3. 함수 실행 및 정보 확인
greet("홍길동")

print("-" * 30)
print(f"함수 이름: {greet.__name__}")       # 원래 이름인 'greet' 출력
print(f"독스트링: {greet.__doc__}")         # 원래 설명인 '사용자에게...' 출력




# 1. @functools.wraps를 쓰지 않고 수동으로 구현한 데코레이터
def my_decorator_manual(func):
    def wrapper(*args, **kwargs):
        print("💡 [전처리] 함수 실행 전")
        result = func(*args, **kwargs)
        print("💡 [후처리] 함수 실행 후")
        return result
    
    # [수동 구현 핵심] functools.update_wrapper를 직접 호출합니다.
    # wrapper 함수에 func 함수의 메타데이터(이름, 독스트링 등)를 복사합니다.
    functools.update_wrapper(wrapper, func)
    
    return wrapper

# 2. 데코레이터 적용
@my_decorator_manual
def greet(name):
    """사용자에게 인사를 건네는 함수입니다."""
    print(f"안녕하세요, {name}님!")

# 3. 테스트 코드
greet("홍길동")
print("-" * 30)
print(f"함수 이름: {greet.__name__}")  # 정상적으로 'greet' 출력
print(f"독스트링: {greet.__doc__}")    # 정상적으로 '사용자에게...' 출력


import book.my_module as my_module

radius = my_module.number_input()

print(my_module.get_circle_area(radius))
print(my_module.get_circumferrence(radius))