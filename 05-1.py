def print_3_times(value, n):
    for i in range(n):
        print(f'count : {i+1} value : f{value}')
        print('count : {} value : {}'.format(i+1, value))
        

print_3_times('sksk',10)


def print1(*value, n=1) :
    for i in value :
        print(i)
    for i in range(n) :
        print(value[0], value[1])

print1('sksksk','sksksksk','aksk',1,3,4,n=3)


def test(my, your,k,j) :
    print(my)
    print(your)



def factorial(n) : 
    result = 1 
    for i in range(1, n+1) :
        result *= i

    return result


for i in range(1,11):
    print(f"{i} : {factorial(i)}")



def re_factorial(n) :
    if n is 1 :
        return 1
    val = re_factorial(n-1)
    print(f"re_factorial({n-1}) : {val}")
    print(f"return value ({val} * {n}) : {val * n}")
    return val * n


print(re_factorial(10))


def fibo(n):
    if n==1 :
        return 1
    if n==2 : 
        return 1

    else: 
        return fibo(n-1) + fibo(n-2)


def call(func):
    func()


def help():
    print('help')


call(help)


def power(i):
    return i*i
def under(i):
    return i < 3
ss = [1,2,3,4,5]
print(list(map(power,ss)))
print(list(filter(under,ss)))


power = lambda x: x*x
under = lambda x: x<3
ss = [1,2,3,4,5]
print(list(map(power,ss)))
print(list(filter(under,ss)))


ss = [1,2,3,4,5]
print(list(map(lambda x: x*x,ss)))
print(list(filter(lambda x: x<3,ss)))


fd = open('test.txt','r')


vv = fd.read()
print(vv)

print()
val = fd.readline()

print(f'vla = {val}')
fd.close()

with open('test.txt','r') as file : 
    while True : 
        kk = file.readline()
        if kk :
            print(kk,end='')
        else:
            break


import random

hangle = list("가나다라마바사아자차카타파하")
print(hangle)
with open('info.txt', 'w', encoding="UTF-8") as fd:
    for i in range(1000):
        
        name = random.choice(hangle) + random.choice(hangle)
        weight = random.randrange(40,100)
        height = random.randrange(140,190)

        fd.write(f"{name},{weight},{height}\n")


result_str = ''
rfd = open('result.txt','w', encoding="UTF-8")

with open('info.txt', 'r', encoding="UTF-8") as fd:
    
    for i in fd:
        (name,weight,height) = i.strip().split(',')

        if (not name) or (not weight) or (not height):
            continue

        bmi = int(weight) / ((int(height) /100) ** 2)

        result = ''
        if 25 <= bmi:
            result = '과체중'
        elif 18.5 <= bmi:
            result = '정상'
        else:
            result = '저체중' 

        rfd.write('이름 : {}\n몸무게 : {}\n키 : {}\nBMI : {}\n결과 : {}\n'.format(name,weight,height,bmi,result))

rfd.close()    


def test():
    print('dk')
    yield 'test'

print('a')
test()

print('b')
test()

print(test())


def test():
    print('a')
    yield 1 
    print('b')
    yield 2
    print('c')

out = test()

print('d')
a = next(out)

print(a)

print('e')
print(next(out))
print('f')

books = [{'title' : 'aaaa','price':1}, {'title' : 'bb','price':2},{'title' : 'cccccccc','price':4},{'title' : 'dsds','price':0}]
print(books)

print(min(books,key=lambda xx : xx['price']))


books.sort(key=lambda xx : xx['price'], reverse=True)

print()
print(books)



a= [1,3,4]

def fucnddd():
    print(a)
    a.append(7)

fucnddd();
print(a)