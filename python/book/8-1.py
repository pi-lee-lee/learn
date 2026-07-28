student11s = [
    {'name':'ja','korean':88,'math':11,'english':13,'science':74},
    {'name':'ja1','korean':88-1,'math':11+1,'english':13+1,'science':74+1},
    {'name':'ja2','korean':88-2,'math':11+2,'english':13+2,'science':74+2},
    {'name':'ja3','korean':88-3,'math':11+3,'english':13+3,'science':74+3},
    {'name':'ja4','korean':88-4,'math':11+4,'english':13+4,'science':74+4},
    {'name':'ja5','korean':88-5,'math':11+5,'english':13+5,'science':74+5},
    {'name':'ja6','korean':88-6,'math':11+6,'english':13+6,'science':74+6},
    {'name':'ja7','korean':88-7,'math':11+7,'english':13+7,'science':74+7}
]

# print('name', 'total', 'avg', sep = '\t')

# for student in students:
#     sum = 0
#     avg = 0
#     count = 0
#     for a in student.values():
#         if type(a) is not str:
#            sum += a
#            count += 1
#     avg = sum/count
#     # print (student['name'], sum, avg, sep='\t' )


def create_student(name, korean, math, english, science):
    return {'name':name,'korean':korean,'math':math,'english':english,'science':science}


class Student:
    def __init__(self, name,korea,math,english,science):
        self.__name = name
        self.korea = korea
        self.math = math
        self.english = english
        self.science = science

    def get_sum(self):
        return self.korea + self.english + self.math + self.science

    def get_avg(self):
        return self.get_sum() / 4

    def __str__(self):
        return '{} : [sum:{}, avg:{}]'.format(self.__name, self.get_sum(), self.get_avg())

    def __eq__(self, value):
        print('__eq')
        if type(value) is not Student:
            raise TypeError('sksksksksksks qudtls')
        return self.name == value.name and self.get_sum() == value.get_sum() and self.get_avg() == value.get_avg()
    def __ne__(self, value):
        return self.name != value.name and self.get_sum() != value.get_sum() and self.get_avg() != value.get_avg()
    def __gt__(self, other):
        pass
    def __ge__(self, other):
        pass

    @classmethod
    def print(self, list):
        if not all(isinstance(man, Student) for man in list):
            raise TypeError('리스트에 스투던트만 있어야함 ') 
        
        for i in list:
            print(i.__name, i.get_sum(), i.get_avg())




import random

random.randrange(0,100)



students = [Student('dkdk',random.randrange(0,100),random.randrange(0,100),random.randrange(0,100),random.randrange(0,100)),
            Student('dkdk1',random.randrange(0,100),random.randrange(0,100),random.randrange(0,100),random.randrange(0,100)),            Student('dkdk666',random.randrange(0,100),random.randrange(0,100),random.randrange(0,100),random.randrange(0,100)),
            Student('dkdk2',random.randrange(0,100),random.randrange(0,100),random.randrange(0,100),random.randrange(0,100)),
            Student('dkdk3',random.randrange(0,100),random.randrange(0,100),random.randrange(0,100),random.randrange(0,100)),
            Student('dkdk4',random.randrange(0,100),random.randrange(0,100),random.randrange(0,100),random.randrange(0,100)),
            Student('dkdk5',random.randrange(0,100),random.randrange(0,100),random.randrange(0,100),random.randrange(0,100)),
            Student('dkdk6',random.randrange(0,100),random.randrange(0,100),random.randrange(0,100),random.randrange(0,100))
            ]
print('0' * 50)
students[0].name = '1'
print(students[0])
Student.print(students)

print('0' * 50)

try:
    if students[0] == str:
        print('ajfdlajfd')
    else:
        print('not ! ')

except Exception as exp : 
    print(exp)
    print(exp.__traceback__.tb_frame)


val = input('input:')

print(int(val))



class Top:
    def do(self):
        print("Top 실행")

class Left(Top):
    def do(self):
        print("Left 시작")
        super().do()  # 다음 순서인 Right로 갑니다 (부모 Top이 아님!)
        print("Left 끝")

class Right(Top):
    def do(self):
        print("Right 실행")
        super().do()

class Child(Left, Right):  # 다중 상속
    def do(self):
        print("Child 시작")
        super().do()
        print("Child 끝")

# 1. 호출 순서(MRO) 확인하기
# [Child -> Left -> Right -> Top -> object] 순서로 일렬 배치됨
print(Child.__mro__)

# 2. 실행 결과
c = Child()
c.do()


class CustomException(BaseException):

    def __init__(self):
        super().__init__()

    def __str__(self):
        error = '내가만든 익셉션 잘나내 \n'
        error += 'exception Line : {}\n{}'.format(self.__traceback__.tb_lineno,self.__traceback__.tb_frame)
        return error


try:
    raise CustomException
except CustomException as exp:
    print(exp)
        
