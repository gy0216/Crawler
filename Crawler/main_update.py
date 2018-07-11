'''
    title : main.py
    author : lgy
    description : crawler main function
'''
'''
    import list
'''
from crawler.EtodayCrawler1 import EtodayCrawler1
import re
import os
import datetime
import time


'''
    input list
'''
url = {'http://www.etoday.co.kr/news/section/subsection.php?MID=2100&page=1': 'stock_finance',
       'http://www.etoday.co.kr/news/section/subsection.php?MID=2200&page=1': 'company',
       'http://www.etoday.co.kr/news/section/subsection.php?MID=1600&page=1': 'female',
       'http://www.etoday.co.kr/news/section/subsection.php?MID=1100&page=1': 'politics_social'}

base_url = 'http://www.Etoday.co.kr'


'''
    method list
'''
def re_bracket(txt):
    text1 = re.sub("\(", "", txt)
    text2 = re.sub("\)", "", text1)

    return text2

def update(crawler,key):

    crawler._init_c(key)

    out = open('out_file/text/' + str(crawler.date)+' '+url.get(key) + '.txt', 'w')
    out1 = open('out_file/text1/' + str(crawler.date)+' '+url.get(key) + '.txt', 'w')
    flag = 0

    d = crawler.date
    t = crawler.time

    olddate = datetime.datetime.combine(d,t)


    while True:
        crawler._sleep(sec=4)
        crawler._init_cur_page()

        for page in crawler._get_list():
            newd = crawler._get_date(page)
            newt = crawler._get_time(page)

            newdate = datetime.datetime.combine(newd,newt)

            if(olddate < newdate) :
                heads = (crawler._get_head(page))
                out.write(heads)
                head_txt = re_bracket(heads)
                out1.write(head_txt)
                bodys = (crawler._get_body(page))
                for j in bodys:
                    # body_enter = re_enter(j)
                    # out.write(body_enter)
                    out.write(j)
                    body_bracket = re_bracket(j)
                    out1.write(body_bracket)
            else :
                flag =1
                break

        if not crawler._next():
            break

        if flag == 1 :
            break

    out.close()
    out1.close()


'''
    main function
'''

def start_loop() :

    crawler = EtodayCrawler1(url=base_url, base_url=base_url)

    while True :
        for i in url.keys() :
            update(crawler,i)
        h = (datetime.datetime.now().hour)
        m = int(datetime.datetime.now().minute)
        crawler.date = datetime.date.today()
        crawler.time = datetime.time(h, m)
        time.sleep(86400)
    #return threading.Timer(10,start_loop).start()

if __name__ == '__main__':
    start_loop()

