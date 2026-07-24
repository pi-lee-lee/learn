#pip install selenium 
#웹 드라이버 브라우져 자동화 도구 설명은 AI에게 

import time
from urllib import request
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import threading


class Trance :
    def __init__(self, src, des):
        self.src_url = src
        self.des_file = des
        self.lock = threading.Lock()  # 락 객체 생성
        self.count = 0 
        self.total = 0

    def tt_worker(self, driver, param):
        driver.get('https://translate.google.com/?sl=auto&tl=ko&text={}&op=translate'.format(param))
        print('\r 현재 번역진행중 {} % ({}/{})'.format((self.count / self.total) * 100, self.count, self.total),end = '') 
        time.sleep(3)
        return driver.execute_script('return document.querySelectorAll(\'textarea\')[1].innerHTML;')

        
    def t_woker(self, driver, item): 
        depth = len([p for p in item.parents if item.name == 'section'])
            
        title_element = item.select_one(':scope > h1, :scope > h2, :scope > h3, :scope > h4, :scope > h5, :scope > h6')
        title = title_element.get_text(strip=True) if title_element else ''

        indent = "  " * depth

        if title:
            title2 = self.tt_worker(driver,title)
            result += f"{indent}{title2}\n"
            with self.lock:
                self.count += 1
            
        p_elements = item.select(':scope > p')

        for p in p_elements:
            contents2 = self.tt_worker(driver, param = p.get_text().strip())
            result += f"{indent}{contents2}\n"
            with self.lock:
                self.count += 1
                        
        return result    


    def b_worker(self, item, fd):
        result = ''

        sel_option = Options()
        
        sel_option.add_argument('--headless=new') #화면 없이 백그라운드 작업
        sel_option.add_argument('--disable-gpu') #gpu안써 
        sel_option.add_argument('--no-sandbox') #보안격리해제
        sel_option.add_argument('--disable-features=EdgeSignin') #마소팝업차단

        driver = webdriver.Edge(options=sel_option)
        driver.get("about:blank")

        self.t_woker(item,fd)

        driver.quit()

        with self.lock:
            fd.write(result)
            fd.flush()


    def h_worker(self):
        response = request.urlopen(self.src_url)

        soup = BeautifulSoup(response.read(), 'html.parser')

        item = soup.select('section')
        total = len(soup.select_one('body').select('h1, h2, h3, h4, h5, h6'))
        total += len(soup.select_one('body').select('p'))

        self.total = total 
        self.count = 1

        return item

    def f_worker(self, work):
        fd = open(self.des_file,'a+',encoding='utf-8')
        work()
        fd.close()

        

    def start(self):
        section = self.h_worker()

        for i in section:
            pass            
           



 

# driver = webdriver.Chrome()
# driver = webdriver.Firefox()
