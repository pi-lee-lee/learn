array = [1,2,3,4]

array.insert(0,0)

array.extend([5,6,7,8])
array.append(9)
print(array)


array.extend([10,11,12])
print(array)

del array[11]
print(array)

temp = array.pop(11)

print(array)
print(temp)


array.extend([11,12,13])
print(array)
del array[11:]
print(array)

array.extend([11,12,13,14,15,16])
print(array)
del array[12:14]
print(array)


print(array.sort(reverse=True))
print(array)


number = [1,2,3,4,5,6,7,8,9]

for i in range(0, len(number)//2) :
    j = number[i*2]
    print(f"i = {i}, j = {j}")
    number[j] = number[j] ** 2

print(number)


numbes = [[1,2,3],[4,5,6,7],[8,9,10,11,12]]

print(len(numbes))

print(numbes)
print(*numbes)



print(number)
print(*number)

numbes.extend(number)
numbes.append(number)
print(numbes)

sss = [number,number]

print(sss)


dic = {
    'name': "7d 건조망고",
    "type": "당절임",
    "ingredient": ["망고","설탕","메타종아아아", "치자자자자자"], 
    "origin":"필리핀"
}

print("name:", dic["name"])

print(dic)

dic['name'] = "8d 건조망고"
dic['price'] = '50000'

print(dic["name"])
print(dic.get('name'))



del dic['name']
print(dic)


print(dic.items)

for i,j in dic.items() :
    print(f"key : {i}, value : {j}")


dic = {
    'name': "7d 건조망고",
    "type": "당절임",
    "ingredient": ["망고","설탕","메타종아아아", "치자자자자자"], 
    "origin":"필리핀"
}

if 'name' in dic :
    print (dic.get('name'))

print(dic.get('ss'))



for i in dic :
    print(dic.get(i))

del dic['name']


numbers=[1,2,6,4,2,3,5,7,8,9,0,8,7,5,4,5,6,7,8,9,1,2,1,3,2,4,5,6,1,1,1,1,1,1,1,1]
counter = {}

for i in numbers :
    if i in counter :
        counter[i] += 1;
    else :
        counter[i] = 1;

dic = {0:1, 1:1, 2:2}


print(counter)
print(dic)


character = {
    'name' : '기사',
    'level' : '12',
    'items' : { 'sword':'불꽃의 검', 'armor':'풀플레이트'},
    'skill' : ['베기', '세게베기', '아주세게베기']
}

for key in character :
    value = character.get(key)
    if type(value) is dict :
        for vkey in value:
            print(f"{vkey} : {value.get(vkey)}")
    elif type(value) is list : 
        for item in value :
            print(f"{key} : {item}")
    else:
        print(f"{key} : {value}")

print()
print()
for key, value in character.items() :
    print(key, value)