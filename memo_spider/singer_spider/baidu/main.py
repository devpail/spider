# -*- coding:utf-8 -*-

# 爬虫总调main函数

import time
import urllib.parse
import db_helper
import html_ChromeDriver
import html_parser
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

class SpiderMain(object):
    startTime = time.time()
    logger.info("开始时间戳：" + str(startTime))

    # 初始化方法
    def __init__(self):
        # 初始化下载器
        self.downloader = html_ChromeDriver.HtmlDownload()
        # 初始化解析器
        self.parser = html_parser.HtmlParser()
        # 初始化数据库存储
        self.dbHelper = db_helper.DbHelper()

    # 抓取歌手名字
    def crawlSinger(self, root_url):
        # 下载url页面html
        soup = self.downloader.download(root_url)
        # print(htmlCode.decode('utf-8'))
        # 解析html代码
        datas = self.parser.parseSinger(soup)
        # 存储到数据库中
        self.dbHelper.saveSinger(datas)

        endTime = time.time()
        totalTime = endTime - self.startTime
        logger.info("抓取歌手url已用时间：" + str(totalTime) + "秒")

    # 抓取百度音乐歌手个人页面的百度百科URL
    def crawlBaseInfo(self):
        # 从数据库中取出所有的歌手
        singers = self.dbHelper.listSinger()
        # 遍历歌手的信息取出百度音乐个人页面
        for singer in singers:
            # 抓取百科地址、贴吧地址、图片地址存储
            html_doc = self.downloader.download(singer[1])
            datas = self.parser.parseBaseInfo(html_doc)
            self.dbHelper.saveBaseInfo(singer[0], datas)

    # 循环遍历、处理页面url集合
    def crawlSingerBaike(self, singers):

        for singer in singers:
            if self.dbHelper.getSingerBaike(singer[1]) != 0:
                logger.info(singer[2] + ' 的百科信息已经被抓取~')
                continue
            logger.info('开始抓取 '+singer[2] + ' 的百科信息~')
            # 下载百度音乐页面
            singer_baike_url = 'https://baike.baidu.com/item/' + urllib.parse.quote(singer[2])
            soup = self.downloader.download(singer_baike_url)
            # logger.info(html_doc.decode(encoding='UTF-8'))
            # 抓取百科页面信息
            itemDatas = self.parser.parseBaike(soup)
            if itemDatas is None:
                logger.info(singer[2] + " 的百科页面-没有所需数据！")
            else:
                # 存储抓取的数据
                logger.info('保存 '+singer[2] + " 的百科信息~")
                self.dbHelper.saveBaike(singer[0], singer_baike_url, soup, itemDatas)

    # 抓取百科词条信息，主要为了抓取生日信息
    def crawlBaike(self):
        # 从数据库中取出所有的名字信息
        singers = self.dbHelper.get10Singer()
        while singers != None:
            self.crawlSingerBaike(singers)
            singers = self.dbHelper.get10Singer()
        else:
            logger.info("url已全部抓取完毕~")



if __name__ == "__main__":
    root_url = "http://music.baidu.com/artist"
    obj_spider = SpiderMain()
    #obj_spider.crawlSinger(root_url)
    # 此方法未完善
    # obj_spider.crawlBaseInfo()
    obj_spider.crawlBaike()
