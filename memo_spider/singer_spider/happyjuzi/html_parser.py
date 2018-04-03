# -*- coding:utf-8 -*-

import re
import uuid
import time
from bs4 import BeautifulSoup
import logging
logger = logging.getLogger()

class HtmlParser(object):
    def getPageURLs(self, soup):
        reDatas = []
        div_tag = soup.find("div", class_="tcdPageCode")
        if(div_tag == None):
            logger.info("未抓取到页面url")
            return None
        a_tags = div_tag.find_all("a")
        for a_tag in a_tags:
            reData={}
            reData['id'] = uuid.uuid1()
            reData['time'] = time.time()
            reData['href'] = a_tag['href']
            reDatas.append(reData)
        return reDatas

    def getStarURLs(self, soup):
        reDatas = []
        div_tag = soup.find("div", class_="result_starlibrary")
        if (div_tag == None):
            logger.info("未抓取到明星url")
            return None
        a_tags = div_tag.find_all("a", class_="name_hotstar")
        # logger.info(a_tags)
        for a_tag in a_tags:
            reData = {}
            reData['id'] = uuid.uuid1()
            reData['name'] = a_tag['title']
            reData['href'] = a_tag['href']
            reData['time'] = time.time()
            reDatas.append(reData)
        return reDatas

    def getStar(self, html_doc):
        reDatas = []
        if html_doc is None:
            return None
        soup = BeautifulSoup(html_doc.decode(encoding='UTF-8'), 'html.parser')
        div_star = soup.find("div", class_="result_starlibrary")
        if div_star is None:
            return None
        a_stars = div_star.find_all("a", class_="name_hotstar")
        for a_star in a_stars:
            reData={}
            reData['id'] = uuid.uuid1()
            reData['time'] = time.time()
            reData['name'] = a_star['title']
            reData['href'] = a_star['href']
            reDatas.append(reData)
        return reDatas


