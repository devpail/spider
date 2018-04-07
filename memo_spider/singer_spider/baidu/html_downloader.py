# -*- coding:utf-8 -*-

from urllib import request
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()
class HtmlDownload(object):
    def download(self, root_url):
        if root_url is None:
            return None
        html = "null"
        try:
            response = request.urlopen(root_url)
            html = response.read()
            logger.info('Status:'+response.status+response.reason)
            if response.status != 200:
                return None
        except Exception as err:
            logger.info(err.__str__())
        return html

    #增加header等请求信息
    def download2(self, root_url):
        if root_url is None:
            return None
        html = None
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            'Host': 'baike.baidu.com'
        }

        req = request.Request(url=root_url,  headers=headers, method='GET')

        try:
            response = request.urlopen(req)
            html = response.read()
            logger.info('Status:'+response.status+response.reason)
            if response.status != 200:
                return None
        except Exception as err:
            logger.info(err.__str__())
        return html
