#pip install selenium 
#웹 드라이버 브라우져 자동화 도구 설명은 AI에게 
#beautiful soup 사이트에 메인 화면을 번역 하여 파일로 작성 하는 샘플 코드 단일 작업으로 지연이 심해 3쓰레드 구성 
#5쓰레드부터는 구글에서 막기도 함 5이상은 무조껀 막힘 로봇 체크 걸리고 한동안 계속 인간이냐 체크 화면 발생 
#추가 작업 필요한것 : 중간에 팅기면 쓰레드 정리 필수

import time
from urllib import request
from selenium import webdriver
# from selenium.webdriver.edge.options import Options
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import threading

from queue import Queue

class Trance :
    NUM_THREAD = 2

    def __init__(self, src, des):
        self.src_url = src
        self.des_file = des
        self.lock = threading.Lock()  # 락 객체 생성
        self.count = 0 
        self.total = 0
        self.task_queues = [Queue() for _ in range(Trance.NUM_THREAD)]
        self.result_queue = Queue()
        self.threads = []
        self.init()
    
    def init(self):

        for i in range(Trance.NUM_THREAD):
            t = threading.Thread(target=self.worker_task, args=(i,self.task_queues[i]))
            t.daemon = True 
            self.threads.append(t)
            t.start()

    def worker_task(self,i, my_queue):
#         sel_option = Options()        

        #firefox
        # sel_option.add_argument('-headless')
        # sel_option.set_preference("identity.fxaccounts.enabled", False)
        # sel_option.set_preference("reader.parse-on-load.enabled", False)
        # sel_option.set_preference("dom.webnotifications.enabled", False)

        #엣지
        # sel_option.add_argument('--headless=new') #화면 없이 백그라운드 작업
        # sel_option.add_argument('--disable-gpu') #gpu안써 
        # sel_option.add_argument('--no-sandbox') #보안격리해제
        # sel_option.add_argument('--disable-features=EdgeSignin') #마소팝업차단
        # driver = webdriver.Edge(options=sel_option)
        
        #chrome
        # sel_option.add_argument('--headless=new')
        # sel_option.add_argument('--disable-gpu')
        # sel_option.add_argument('--no-sandbox')
        # # 크롬 전용: 상단에 "자동화된 테스트 소프트웨어에 의해 제어되고 있습니다" 알림창 제거
        # sel_option.add_experimental_option("excludeSwitches", ["enable-automation"])
        # sel_option.add_experimental_option('useAutomationExtension', False)
    
    
        driver = webdriver.Firefox()
        driver.get("about:blank")    
        
        while True:
            task_packet = my_queue.get()
            
            if task_packet is None:
                my_queue.task_done()
                break

            task_id, data = task_packet
            result = self.trance_worker(driver,data)
            self.result_queue.put((task_id, result))
                               
            # 큐 작업 완료 알림
            my_queue.task_done()

        
    def trance_worker(self, driver, param):
        driver.get('https://translate.google.com/?sl=auto&tl=ko&text={}&op=translate'.format(param))
        time.sleep(5)
        return driver.execute_script('return document.querySelectorAll(\'textarea\')[1].innerHTML;')

    
    def divide_woker(self, l_elements):
        task_id = 0
        for element in l_elements:    
            title_element = element.select_one(':scope > h1, :scope > h2, :scope > h3, :scope > h4, :scope > h5, :scope > h6')
            title = title_element.get_text(strip=True) if title_element else None

            if title:
                target_queue_idx = task_id % Trance.NUM_THREAD
                self.task_queues[target_queue_idx].put((task_id, title))
                task_id += 1
            else :    
                p_elements = element.select(':scope > p')
                for p in p_elements:
                    target_queue_idx = task_id % Trance.NUM_THREAD
                    self.task_queues[target_queue_idx].put((task_id, p.get_text().strip()))
                    task_id += 1

        for q in self.task_queues:
            q.join()

        
    def html_worker(self):
        response = request.urlopen(self.src_url)
        soup = BeautifulSoup(response.read(), 'html.parser')
        l_elements = soup.select('section')

        total = len(soup.select_one('body').select('h1, h2, h3, h4, h5, h6'))
        total += len(soup.select_one('body').select('p'))

        self.total = total 
        self.count = 1

        return l_elements

    
    def file_worker(self):
        pass

    
    def start(self, src_url, des_file):
        with open(self.des_file,'a+',encoding='utf-8') as fd:

            elements = self.html_worker()
            self.divide_woker(elements)
            unsorted_results = []
            while not self.result_queue.empty():
                unsorted_results.append(self.result_queue.get())

            unsorted_results.sort(key=lambda item: item[0])
            final_ordered_results = [result for task_id, result in unsorted_results]

            for i in range(10): # 상위 10개만 출력 확인
                print(f"[order {i}] -> {final_ordered_results[i]}")

            for i in final_ordered_results:
                fd.write(i)
            fd.flush()
            

        for q in self.task_queues:
            q.put(None)


            
k = Trance('https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup','temp.txt')                            
k.start('https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup','temp.txt')  
#  
# driver = webdriver.Chrome()
# driver = webdriver.Firefox()
