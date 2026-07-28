from urllib import request 
import ssl
import certifi


context = ssl.create_default_context(cafile=certifi.where())


target = request.urlopen('https://www.hanbit.co.kr/images/common/logo_hanbit.png', context=context)

file = open ('image.png','wb')
file.write(target.read())
file.close()