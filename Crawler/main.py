"""
    title : main.py
    author : lgy
"""

"""
    import
"""
import sys #for arg in main
from crawler.EtodayCrawler1 import EtodayCrawler1
import re
import os
import datetime
import time

"""
    variable
"""
url = {'http://www.etoday.co.kr/news/section/subsection.php?MID=2100&page=1': 'stock_finance',
       'http://www.etoday.co.kr/news/section/subsection.php?MID=2200&page=1': 'company',
       'http://www.etoday.co.kr/news/section/subsection.php?MID=1600&page=1': 'female',
       'http://www.etoday.co.kr/news/section/subsection.php?MID=1100&page=1': 'politics_social'}

base_url = 'http://www.Etoday.co.kr'

OUT_PATH = "out_file/"

TXT = ".txt"

"""
    functions
"""
def updateTime():
    h = datetime.datetime.now().hour
    m = datetime.datetime.now().minute
    return datetime.date.today(), datetime.time(h, m)

def UMode(update_delay = (60 * 60 * 24)):
    _d, _t = updateTime()
    crawler = EtodayCrawler1(url=i, next='&page=1', decode='utf8', base_url=base_url)

    while True :
        for i in url.keys() :
            update(crawler, i)
        crawler.date, crawler.time = updateTime()
        time.sleep(update_delay)

def update(crawler, category):
    crawler._init_c(category)

    out = open(OUT_PATH + "text/" + str(crawler.date) + ' ' + url.get(category) + TXT, 'w')
    flag = 0

    d = crawler.date
    t = crawler.time

    old_date = datetime.datetime.combine(d,t)


    while True:
        crawler._sleep(sec=4)
        crawler._init_cur_page()

        for page in crawler._get_list():
            new_d, new_t = crawler._get_datetime(page)
            new_date = datetime.datetime.combine(new_d, new_t)

            if(old_date < new_date) :
                heads = crawler._get_head(page)
                out.write(heads)
                bodys = crawler._get_body(page)
                for j in bodys:
                    out.write(j)
            else:
                flag = 1
                break

        if not crawler._next():         break
        if flag is 1:                   break

    out.close()
        

######################################

def loop(crawler, key):
    out = open(OUT_PATH + "text/" + url.get(key) + TXT, 'w')
    out_html = open(OUT_PATH + "html/" +url.get(key) + TXT, 'a')
    while True:
        crawler._sleep(sec = 4)
        crawler._init_cur_page()

        for page in crawler._get_list():
            heads= crawler._get_head(page)
            out.write(heads)
            bodys= crawler._get_body(page)

            # print(page + " "+ heads)
            out_html.write(page + " "+ heads + "\n")

            for j in bodys :
                out.write(j)

        if not crawler._next():
            break

    out.close()
    out_html.close()


def BMode():
    for i in url.keys() :
        crawler = EtodayCrawler1(url=i, next='&page=1', decode='utf8', base_url=base_url)
        loop(crawler,i)

######################################

def main():
    args = len(sys.argv) - 1
    if not(args is 1):
        usgae()
        sys.exit()
    
    _ar = sys.argv[1]

    if _ar == "-u":
        UMode()
    elif _ar == "-b":
        BMode()
    


def usgae():
    print("""python <option>

    option:
    -u : get up-to-date news
    -b : get before news""")

if __name__ == "__main__":
    main()