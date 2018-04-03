# -*- coding:utf-8 -*-

import re
import uuid
import time
from bs4 import BeautifulSoup


class HtmlParser(object):
    def parseSinger(self, htmlCode):
        reDatas = []
        if htmlCode is None:
            return None
        soup = BeautifulSoup(htmlCode, 'html.parser')
        ul_tag = soup.find("ul", class_="container")
        a_tags = ul_tag.find_all("a", href=re.compile(r"/artist/"))
        # print(a_tags)
        for a_tag in a_tags:
            if a_tag.has_attr('title'):
                reData = {}
                reData['id'] = uuid.uuid1()
                reData['time'] = time.time()
                reData['href'] = 'http://music.baidu.com' + a_tag['href']
                reData['name'] = a_tag['title']
                reData['site'] = 'http://music.baidu.com/artist'
                reDatas.append(reData)
                # print(reData)
        return reDatas

    def parseBaseInfo(self, html_doc):
        # TODO
        return None

    def parseBaike(self, html_doc):
        reDatas = []
        if html_doc is None:
            return None
        soup = BeautifulSoup(html_doc.decode(encoding='UTF-8'), 'html.parser')
        div_baseinfo = soup.find("div", class_="basic-info")
        if div_baseinfo is None:
            return None
        dt_names = div_baseinfo.find_all("dt", class_="basicInfo-item name")
        for index, dt_name in enumerate(dt_names):
            rsData={}
            rsData['order'] = index
            rsData['name'] = dt_name.get_text().replace('\xa0', '').strip('\n')
            dd_value = dt_name.find_next()
            rsData['value'] = dd_value.get_text().replace('\xa0', '').strip('\n')
            reDatas.append(rsData)
        #dd_values = dt_names.find_next()
        print(reDatas)
        return reDatas
