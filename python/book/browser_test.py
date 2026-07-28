#pip install selenium 
#웹 드라이버 브라우져 자동화 도구 설명은 AI에게 

import time
from urllib import request
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup

response = request.urlopen('https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup')

# driver = webdriver.Chrome()
# driver = webdriver.Firefox()

sel_option = Options()

sel_option.add_argument('--headless=new') #화면 없이 백그라운드 작업
sel_option.add_argument('--disable-gpu') #gpu안써 
sel_option.add_argument('--no-sandbox') #보안격리해제
sel_option.add_argument('--disable-features=EdgeSignin') #마소팝업차단

# driver = webdriver.Edge(options=sel_option)
driver = webdriver.Firefox()
result = '' 
count = 0 

soup = BeautifulSoup(response.read(), 'html.parser')
section = soup.select('section')
total = len(soup.select_one('body').select('h1, h2, h3, h4, h5, h6'))
total += len(soup.select_one('body').select('p'))

count = 1
fd = open('web.txt','w',encoding='utf-8')

for i in section:
    depth = len([p for p in i.parents if p.name == 'section'])
    
    title_element = i.select_one(':scope > h1, :scope > h2, :scope > h3, :scope > h4, :scope > h5, :scope > h6')
    title = title_element.get_text(strip=True) if title_element else ''

    indent = "  " * depth

    if title:
        driver.get('https://translate.google.com/?sl=auto&tl=ko&text={}&op=translate'.format(title))
        print('\r 현재 번역진행중 {} % ({}/{})'.format(100/total*count, count, total),end = '') 
        time.sleep(3)
        title2 = driver.execute_script('return document.querySelectorAll(\'textarea\')[1].innerHTML;')
        count += 1
        fd.write(f"{indent}{title2}\n")
        fd.flush()


    p_elements = i.select(':scope > p')
    for p in p_elements:
        driver.get('https://translate.google.com/?sl=auto&tl=ko&text={}&op=translate'.format(p.get_text(strip=True)))
        print('\r 현재 번역진행중 {} % ({}/{})'.format(100/total*count, count, total),end = '') 
        time.sleep(3)
        contents = indent + ' '
        contents2 = driver.execute_script('return document.querySelectorAll(\'textarea\')[1].innerHTML;')
        count += 1
        fd.write(f"{indent}{contents2}\n")
        fd.flush()

fd.close()    
driver.quit()