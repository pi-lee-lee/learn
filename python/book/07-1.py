import random as r, math as m
from math import sqrt as __sqrt

print(r.random())

print(m.sqrt(2))
print(__sqrt(2))

print(r.uniform(10.0, 20.0))

print(r.randrange(1, 100))

print(r.sample([1,2,3,4,5,6,7],1))

from random import random as r, randrange, choice, uniform as u, sample as s

print(r())

print(u(10.0, 20.0))

print(randrange(1, 100))

print(s([1,2,3,4,5,6,7],1))

import random

import os as mycom

mycom.system('dir')

import subprocess as mymy

mymy.run("dir",shell=True)


from urllib import request

target = request.urlopen('https://google.com')

# fd = open('google.html','w')
# fd.write(str(target.read()))
# fd.close()


from bs4 import BeautifulSoup

soup = BeautifulSoup(target, 'html.parser')

print(soup.body)


