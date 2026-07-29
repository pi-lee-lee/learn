print("{:3}".format(1))
print("{:=3}".format(1))
print()
print("{:+5d}".format(1222))
print("{:+5d}".format(-1222))
print()
print("{:+5d}".format(12))
print("{:+5d}".format(-12))
print("{:=+5d}".format(12))
print("{:=+5d}".format(-12))
print()

print("{:+010d}".format(1222))
print("{:+010d}".format(-1222))
print("{:=010d}".format(1222))
print("{:=010d}".format(-1222))
print("{:10d}".format(1222))
print("{:10d}".format(-1222))
print("{:+10d}".format(1222))
print("{:+10d}".format(-1222))
print("{:=+10d}".format(1222))
print("{:=+10d}".format(-1222))


print("float  {:.3f}".format(13.232323))
print("floatg {:7g}".format(13.239492900000000000000)) #g는 그냥 글자 카운트됨 

ssss = "      slkdjflskjdfljsd sdljfslkdjf          "
print(ssss.strip())
print(ssss.lstrip())
print(ssss.rstrip())

"s".isprintable


print("pos {}".format("abc,abc,abc,add".find("abc")))
print("pos {}".format("abc,abc,abc,add".rfind("abc")))


print("\"abc\" in \"abc,abc,abc,add\" : ","abc" in "abc,abc,abc,add" )
print("\"d\" in \"abc,abc,abc,add\" : ","d" in "abc,abc,abc,add" )
print("\"z\" in \"abc,abc,abc,add\" : ","z" in "abc,abc,abc,add" )

print("\"abc,abc,abc,add\".split(\",\") = ", "abc,abc,abc,add".split(","))
print("\"abc,abc,abc,add\".split(\",\")[0] = ", "abc,abc,abc,add".split(",")[0])
print("\"abc,abc,abc,add\".split(\",\")[0:1] = ","abc,abc,abc,add".split(",")[0:1])
print("\"abc,abc,abc,add\".split(\",\")[0:2] = ","abc,abc,abc,add".split(",")[0:2])
print("\"abc,abc,abc,add\".split(\",\")[0:3] = ","abc,abc,abc,add".split(",")[0:3])
print("\"abc,abc,abc,add\".split(\",\")[0:4] = ","abc,abc,abc,add".split(",")[0:4])
print("\"abc,abc,abc,add\".split(\",\")[1:0] = ","abc,abc,abc,add".split(",")[1:0])
print("\"abc,abc,abc,add\".split(\",\")[1:1] = ","abc,abc,abc,add".split(",")[1:1])
print("\"abc,abc,abc,add\".split(\",\")[1:2] = ","abc,abc,abc,add".split(",")[1:2])
print("\"abc,abc,abc,add\".split(\",\")[1:3] = ","abc,abc,abc,add".split(",")[1:3])
print("\"abc,abc,abc,add\".split(\",\")[1:4] = ","abc,abc,abc,add".split(",")[1:4])
print("\"abc,abc,abc,add\".split(\",\")[2:0] = ","abc,abc,abc,add".split(",")[2:0])
print("\"abc,abc,abc,add\".split(\",\")[3:0] = ","abc,abc,abc,add".split(",")[3:0])
print("\"abc,abc,abc,add\".split(\",\")[4:0] = ","abc,abc,abc,add".split(",")[4:0])
print("\"abc,abc,abc,add\".split(\",\")[0:-1] = ","abc,abc,abc,add".split(",")[0:-1])
print("\"abc,abc,abc,add\".split(\",\")[0:-2] = ","abc,abc,abc,add".split(",")[0:-2])
print("\"abc,abc,abc,add\".split(\",\")[0:-3] = ","abc,abc,abc,add".split(",")[0:-3])
print("\"abc,abc,abc,add\".split(\",\")[0:-4] = ","abc,abc,abc,add".split(",")[0:-4])
print("\"abc,abc,abc,add\".split(\",\")[0:0] = ","abc,abc,abc,add".split(",")[0:0])

k = 7 

print(f"3+7 ={3+k**2}")

#문제 1

# r2 = input("구의 반지름을 입력해주세요: ")

# print(f"= 구의 부피는 {int(r2)**3 * 3.141592 * 4/3}")
# print(f"= 구의 겉넓이는 {int(r2)**2 * 3.141592 * 4}")

#문제2 

# u = input("밑변의 길이를 입력해주세요 : ")
# h = input("높이의 길이를 입력해주세요 : ")

# print("빗변의 길이는 {}".format((float(u)**2 + float(h)**2) ** (1/2)))

import sys

print(sys.version)

from sql_metadata import Parser

query = "SELECT column_name FROM information_schema.COLUMNS WHERE table_schema = DATABASE() AND table_name = {}  ORDER BY ordinal_position;"
print(Parser(query).tables[0])
print(query[query.upper().find('FROM') + 4:].lstrip())