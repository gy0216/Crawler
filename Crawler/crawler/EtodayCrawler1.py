'''
    Title : TennisCrawler.py
    Author : lgy
'''

'''
    import list
'''

'''
    class : EtodayCrawler1
'''
from crawler.BaseCrawler import BaseCrawler
import re
import datetime
from datetime import time

class EtodayCrawler1(BaseCrawler):
    def __init__(self, url, next, decode, base_url=None):
        self.base_url = base_url if base_url else url
        self.next_url = next
        self.decode = decode
        super().__init__(url)


    def _next(self):
        if (len(self.bs.find_all('a', {'class': 'next'}))==0) :
            return False

        from_change = int(re.findall('\d+',self.next_url)[0])
        to_change = from_change+1
        next_url = self.next_url.replace(str(from_change),str(to_change))
        new_url = self.url.replace(str(self.next_url), str(next_url))
        self.next_url = next_url
        self.url = new_url
        return True

    def _get_list(self):
        item_list = self.bs.find('ul', {'class': 'news_lst2'})

        ret_list = [self.base_url + tit.find('a').get('href')
                    for tit in item_list.find_all('p', {'class': 'summary'})]
        """
        print("---------")
        [print(i) for i in ret_list]
        print("========")
"""
        return ret_list

    def delBlank(self, txt=""):
        """
        """
        t = txt.strip()

        return t

    def re_enter(txt):
        text = re.sub("다\.", "다.\n", txt)

        return text

    

    def _get_head(self, page):
        bs = self._init_bs(page)
        head = bs.find_all("title")
        return head[0].text

    def _get_body(self, page):
        bs = self._init_bs(page)
        body = bs.find('div', {'id': 'newsContent'})
        line_lst = body.find_all("p")
        # line_lst = [line.text.strip() for line in line_lst if line.text.strip() != '']
        temp_text = ""
        #[temp_text += s for s in line_lst]
        for asd in line_lst:
            temp_text += asd.text
        temp_list = temp_text.split("다.")
        #line_lst = [line.strip() for line in temp_list if line.strip() != '']
        return_value = []
        for s in temp_list:
            #print(len(s), type(s), s)
            if len(s) is 0:
                continue
            return_value.append(self.delBlank(s) + "다.\n")

        #return line_lst
        return return_value

    # def _get_date(self,page):
    #     bs = self._init_bs(page)
    #     t1 = bs.find('div',{'class':'byline'})
    #     t2 = t1.find('em').text
    #     date =re.findall('\d+', t2)
    #     year = int(date[0])
    #     month =int(date[1])
    #     day = int(date[2])

    #     return datetime.date(year,month,day)


    # def _get_time(self,page):
    #     bs = self._init_bs(page)
    #     t1 = bs.find('div', {'class': 'byline'})
    #     t2 = t1.find('em').text
    #     t = re.findall('\d+', t2)
    #     hour = int(t[3])
    #     minute = int(t[4])

    #     return datetime.time(hour,minute)


    def _get_datetime(self, page):
        bs = self._init_bs(page)
        t1 = bs.find('div',{'class':'byline'})
        t2 = t1.find('em').text
        date =re.findall('\d+', t2)
        year = int(date[0])
        month =int(date[1])
        day = int(date[2])
        hour = int(date[3])
        minute = int(date[4])

        return datetime.date(year,month,day), datetime.time(hour,minute)

    def _init_c(self,page) :
        self.url = page
        self.heads = []
        self.bodys = []
        self.next_url = '&page=1'
        self.file_name = 1