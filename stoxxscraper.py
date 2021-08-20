import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from queue import Queue
from threading import Thread
from selenium.webdriver.common.by import By
import pandas as pd
import time

def get_comp_names(b, i):
    b.execute_script(f"javascript:paginateList(jsPaginationURL, 'componentViewSearchResult', '{i}');")
    time.sleep(1)
    tbody = b.find_element(By.CLASS_NAME,'custom-sorted-table.width100p').find_element(By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.TAG_NAME, 'tr')

    for row in rows:
        name = row.find_elements(By.TAG_NAME,'td')[0]
        link = name.find_element(By.TAG_NAME,'a').get_attribute('href')
        subsector = get_comp_subsector(link,bqueue)
        result[name.text] = [subsector]
        print(f'{name.text}: {result[name.text]}')

def get_comp_subsector(link,q):
    brow = q.get()
    brow.get(link)
    subsector = brow.find_element(By.CLASS_NAME,'last').find_elements(By.TAG_NAME,'td')[1]
    q.task_done()
    q.put(brow)
    return subsector.text
    

def scrap(b,q):
    while not q.empty():
        print(q.get())
        get_comp_names(b,q.get())
        q.task_done()

options = Options()
options2 = Options()
result = {}
queue = Queue(maxsize=0)
bqueue = Queue(maxsize=0)
n_threads = 16

options.add_argument("--headless")
options.add_argument("--log-level=3")

options2.add_experimental_option("detach", True)
options2.add_argument("--headless")
options2.add_argument("--log-level=3")

b1 = webdriver.Chrome(options=options2)
bqueue.put(b1)
b2 = webdriver.Chrome(options=options2)
bqueue.put(b2)
b3 = webdriver.Chrome(options=options2)
bqueue.put(b3)
b4 = webdriver.Chrome(options=options2)
bqueue.put(b4)
b5 = webdriver.Chrome(options=options2)
bqueue.put(b5)
b6 = webdriver.Chrome(options=options2)
bqueue.put(b6)
b7 = webdriver.Chrome(options=options2)
bqueue.put(b7)
b8 = webdriver.Chrome(options=options2)
bqueue.put(b8)
b9 = webdriver.Chrome(options=options2)
bqueue.put(b9)
b10 = webdriver.Chrome(options=options2)
bqueue.put(b10)
b11 = webdriver.Chrome(options=options2)
bqueue.put(b11)
b12 = webdriver.Chrome(options=options2)
bqueue.put(b12)
b13 = webdriver.Chrome(options=options2)
bqueue.put(b13)
b14 = webdriver.Chrome(options=options2)
bqueue.put(b14)
b15 = webdriver.Chrome(options=options2)
bqueue.put(b15)
b16 = webdriver.Chrome(options=options2)
bqueue.put(b16)

for i in range(1,1069):
    queue.put(i)

for i in range(n_threads):
    b = webdriver.Chrome(options=options)
    b.get('https://www.stoxx.com/search-result?p_p_id=STOXX_Search_WAR_STOXXSearchportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_STOXX_Search_WAR_STOXXSearchportlet_searchTerm=***&_STOXX_Search_WAR_STOXXSearchportlet_action=search&_STOXX_Search_WAR_STOXXSearchportlet_type=components')
    worker = Thread(target=scrap, args=(b, queue,))
    worker.start()

while threading.active_count() > 1:
    pass
df = pd.DataFrame().from_dict(result).transpose()
df = df.sort_index(axis = 0)
df.to_excel('stoxxresult.xlsx')