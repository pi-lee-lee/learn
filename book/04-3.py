k = range(7)

print(k)

k2 = list(range(1,101))

print(k2)
print(k2[::-1])

#높이에 따라 lengh는 2n-1 
#공백은 양쪽은 각각   n-1

print("    *    ") #1 2n+1, n-1 * 2,  
print("   ***   ") #3
print("  *****  ") #5
print(" ******* ") #7
print("*********") #9 

height = 7

for floor in range(height) :
    space = "";
    star = "";
    for s in range(height-1-floor) : 
        space += " "
    for s2 in range(floor*2+1) :
        star += "*"
    print(space + star)

for floor in reversed(range(height-1)) :
    space = "";
    star = "";
    for s in range(height-1-floor) : 
        space += " "
    for s2 in range(floor*2+1) :
        star += "*"
    print(space + star)


board = ""
icon = "*"
licon = "["
ricon = "]"
for floor in range(height) :
    board += licon * (height-1-floor)
    board += icon * (floor*2+1)
    board += ricon * (height-1-floor)
    board += '\n'

for floor in reversed(range(height-1)) :
    board += licon * (height-1-floor)
    board += icon * (floor*2+1)
    board += ricon * (height-1-floor)
    board += '\n'
print(board)


list_test = [1,2,2,2,2,2,2,2,2,2,2,3]

value = 2

print(list_test.remove(2))
print(list_test)

for value in list_test:
    print(value)


while value in list_test:
    list_test.remove(value)

print(list_test)


import time

time.sleep(0.1);


for i in range(20):
    print(time.time())


print(f"time + 5 = {time.time()+5}, time = {time.time()} ")



numbers = [5,6,15,20,7,25]

count = 0

print(f"{numbers[++count]}, {numbers[++ count]}")

while True:
    count += 1
    if count < len(numbers) :
        pass
    else:
        break
    if numbers[count] %2 == 0 :
        print("짝수")
    else:
        continue 
    print(numbers[count])
        
max_value = 0
a = 0
b = 0 
init = 100

for i in range(init):
    j = init -i
    if max_value < i*j :
        max_value = i*j
        a= i 
        b= j

print("최대가 되는 경우 : {} * {} = {}".format(a,b,max_value))
    

text = ['100','20','30','40','10']



print(max(text))
print(min(text))
print(text)
reversed(text)
print(text)
print(list(reversed(text)))

for i in range(10):
    print(i)

for i in reversed(range(100)):
    print(i)



example_list = ['요소1', '요소2', '요소3']

print('# 단순출력')
print(example_list)
print()


print('# enumerate() 함수 적용 출력')
print(enumerate(example_list))
print()


print('# list(0 함수로 강제 변환 출력')
print(list(enumerate(example_list)))
print()

print('#반복문과 조합하기')
for i, value in enumerate(example_list):
    print("{}요소는 {}입니다.".format(i,value))


array = ['tkrhk', 'wken', 'chzhfflt', 'qksksk', 'cpfl']

output = [fruit for fruit in array if fruit == 'chzhfflt' or fruit == 'wken' or fruit == 'tkrhk']
output2 = [fruit for fruit in array if fruit != 'chzhfflt' and fruit != 'wken' and fruit != 'tkrhk']

print(output)
print(output2)


number = 10

if number %2 == 0 :
    print((f"d입력한 {number}문제열은\n"
          "나나나나\n "
          "니ㅏㅇ리넝ㄹ\n" ))         




#문제 
number = [1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4]
ddd = {}
for i in number :
    if ddd.get(i) :
        ddd[i] += 1
    else:
        ddd[i] = 1

print (ddd);

aa = "sldjflajfdlaksjfdasodufhosahdfosahfdoshaofdhsahfsldjflajfdlaksjfdasodufhosahdfosahfdoshaofdhsahfeez"

ddd = {}
for i in aa :
    if ddd.get(i) :
        ddd[i] += 1
    else:
        ddd[i] = 1

print (ddd);

print (aa[0:3], aa[3:6])

ddd = {}
for i in range(len(aa)//3) :
    pos = i*3 
    item = aa[pos:pos+3]

    if ddd.get(item) :
        ddd[item] += 1
    else:
        ddd[item] = 1

print(ddd)



numbers = [1,2,[3,4],5,[6,7,8],9]
temp = []
print(numbers)


for i in numbers:
    
    if type(i) is list:
        temp.extend(i)
    else:
        temp.append(i)

        

print(temp)