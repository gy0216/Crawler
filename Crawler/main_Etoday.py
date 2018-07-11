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


'''
    input list
'''
url = {'http://www.etoday.co.kr/news/section/subsection.php?MID=2100&page=2':'증권_금융',
       'http://www.etoday.co.kr/news/section/subsection.php?MID=2200&page=2':'기업',
       'http://www.etoday.co.kr/news/section/subsection.php?MID=1600&page=2':'여성',
       'http://www.etoday.co.kr/news/section/subsection.php?MID=1100&page=2':'정치_사회'}

base_url = 'http://www.Etoday.co.kr'


'''
    method list
'''
def re_bracket(txt):
    text1 = re.sub("\(", "", txt)
    text2 = re.sub("\)", "", text1)

    return text2
def loop(crawler,key):
    out = open('out_file/text/'+url.get(key) + '.txt', 'w')
    out1 = open('out_file/text1/'+url.get(key) + '.txt', 'w')
    while True:
        crawler._sleep(sec=4)
        crawler._init_cur_page()

        out_html = open('out_file/html/'+url.get(key)+' '+str(crawler.file_name)+'.html','w')

        for i in crawler.bs :
            out_html.write(str(i))

        crawler.file_name = crawler.file_name+1

        out_html.close()

        for page in crawler._get_list():
            heads=(crawler._get_head(page))
            out.write(heads[0])
            head_txt=re_bracket(heads[0])
            out1.write(head_txt)
            bodys=(crawler._get_body(page))
            for j in bodys :
                #body_enter = re_enter(j)
                #out.write(body_enter)
                out.write(j)
                body_bracket = re_bracket(j)
                out1.write(body_bracket)


        if not crawler._next():
            break


    out.close()
    out1.close()

'''
    main function
'''
if __name__ == '__main__':
    for i in url.keys() :
        crawler = EtodayCrawler1(url=i, next='&page=1', decode= 'utf8', base_url=base_url)
        loop(crawler,i)

