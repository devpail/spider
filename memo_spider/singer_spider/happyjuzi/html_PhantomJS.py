# -*- coding:utf-8 -*-

from urllib import request
from selenium import webdriver
from bs4 import BeautifulSoup
import logging
logger = logging.getLogger()

class HtmlDownload(object):
    def download(self, root_url):
        if root_url is None:
            return None
        try:
            driver = webdriver.PhantomJS()
            driver.set_page_load_timeout(30)
            driver.get(root_url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            return soup
        except Exception as err:
            logger.info(err.__str__())
        return None

    #增加header等请求信息
    def download2(self, root_url):
        if root_url is None:
            return None
        html = None
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': '_uab_collina=151219112477442719522814; td_cookie=18446744071346496207; _uab_collina=151219118584648068687436; td_cookie=18446744069933399907; _ga=GA1.2.90192142.1512191073; acw_tc=AQAAABwRyWmgbQQAA5E52lP9nconoUb0; _gid=GA1.2.781567232.1513865781; Hm_lvt_aba7c981bd757402fc23fa14ae4c7708=1512191073,1513001684,1513602901,1513865781; Hm_lvt_2d02af1a29752dc3c0b9e49f97d041ef=1512191073,1513001684,1513602901,1513865781; acw_sc__=5a3bc2694b22bdcb724e479c5f6c7a2089d897ec; _gat=1; u_asec=099%23KAFEu7EKEqYEJETLEEEEEpEQz0yFD6tHZXlMa6DJDus4W6zESuwMC6AwSr0XE7EFbOR5DFMTEEylEcZdt3ihE7ErbLa5Dw7WadVE99rqrsbtaEOcz6SDrNEq3MesDzXVaGzclylpNaLll%2FQt%2Fq%2BZ6NGTEELlluaoL9U51rQTEEMFluutG%2FJbE7EUlllP%2F3iSlGnllu%2But37FK%2FllWcOStELllllUO%2FiS13lllu%2Brt37IluYTEHI3iNGE5DoZbHw%2BB1W2ZZpsIlo%2Bp7P05c6kWhmrZHD8bhkgk8ikwN2IKsT2cHf3pMNuViqnhjfuViL%2BMDDfwwLP2UNSqqA63INuViqQkTfuViLPlYFETJDovlv5E7EFlllbr7%3D%3D; Hm_lpvt_aba7c981bd757402fc23fa14ae4c7708=1513866332; Hm_lpvt_2d02af1a29752dc3c0b9e49f97d041ef=1513866332',
            'Host': 'www.happyjuzi.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        }

        req = request.Request(url=root_url,  headers=headers, method='GET')

        try:
            response = request.urlopen(req)
            html = response.read()
            logger.info('Status:', response.status, response.reason)
            if response.status != 200:
                return None
        except Exception as err:
            logger.info(err.__str__())
        return html
