# -*- coding:utf-8 -*-

import time
import logging
import logging.config
import html_PhantomJS
import db_helper
import html_parser
import const

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

# 爬虫总调main函数
class SpiderMain(object):

    pageUrlNum = 0
    starUrlNum = 0
    startTime = time.time()
    logger.info("开始时间戳：" + str(startTime))

    # 初始化方法
    def __init__(self):
        # 初始化下载器
        self.downloader = html_PhantomJS.HtmlDownload()
        # 初始化解析器
        self.parser = html_parser.HtmlParser()
        # 初始化数据库存储
        self.dbHelper = db_helper.DbHelper()

    # 抓取明星
    def crawlMain(self, root_url):
        #1.抓取第一个url页面的信息
        self.crawlPageURL(root_url)
        # 2.遍历抓取数据库中未成功抓取的url页面
        pageUrls = self.dbHelper.select10PageURL()
        while pageUrls != None:
            self.crawlPageURLs(pageUrls)
            pageUrls = self.dbHelper.select10PageURL()
        else:
            logger.info("url已全部抓取完毕~")
        # 3.抓取明星信息
        starUrls = self.dbHelper.select10StarURL()
        while starUrls != None:
            self.crawlStarURLs(starUrls)
            starUrls = self.dbHelper.select10StarURL()


    # 循环遍历、处理明星页面url集合
    def crawlStarURLs(self, starUrls):
        for starUrl in starUrls:
            self.starUrlNum += 1
            logger.info("开始抓取第" + str(self.starUrlNum) + "个starURL - " + starUrl[1])
            # url抓取，返回-2,-1,1
            crawlResult = self.crawlStarInfo(starUrl[1])
            # 更新url抓取状态
            self.dbHelper.updateStarUrlStatus(starUrl[0], crawlResult)
            endTime = time.time()
            totalTime = endTime - self.startTime
            logger.info("抓取url链接已用时间：" + str(totalTime) + "秒")

    def crawlStarInfo(self, url):
        # 下载url页面html
        soup = self.downloader.download(url)
        if soup == None:
            return const.CRAWL_HTML_FAILED
        #
        #TODO
        return const.CRAWL_PAGEURL_SUCCESS

    # 循环遍历、处理页面url集合
    def crawlPageURLs(self, pageUrls):
        for pageUrl in pageUrls:
            self.pageUrlNum += 1
            logger.info("开始抓取第" + str(self.pageUrlNum) + "个pageURL - " + pageUrl[1])
            #url抓取，返回-2,-1,1
            crawlResult = self.crawlPageURL(pageUrl[1])
            # 更新url抓取状态
            self.dbHelper.updatePageUrlStatus(pageUrl[0], crawlResult)
            endTime = time.time()
            totalTime = endTime - self.startTime
            logger.info("抓取url链接已用时间：" + str(totalTime) + "秒")


    # 处理单个url,返回抓取状态
    #-1：抓取失败；0：
    def crawlPageURL(self, url):
        # 下载url页面html
        logger.info("开始抓取页面信息")
        soup = self.downloader.download(url)
        if soup == None:
            return const.CRAWL_HTML_FAILED
        # 处理下面的pageURL链接
        # 获取页面中的url进行保存
        pageUrls = self.parser.getPageURLs(soup)
        if pageUrls == None:
            return const.CRAWL_PAGEURL_FAILED
        # 保存啊保存   先查询url抓取状态,
        self.dbHelper.savePageURLs(pageUrls)
        # 处理页面上的明星信息
        # 解析html代码，保存明星页面链接
        starUrls = self.parser.getStarURLs(soup)
        if starUrls == None:
            return const.CRAWL_PAGEURL_FAILED
        # 存储到数据库中
        self.dbHelper.saveStarURLs(starUrls)
        return const.CRAWL_PAGEURL_SUCCESS



if __name__ == "__main__":
    root_url = "http://www.happyjuzi.com/star-ku/"
    obj_spider = SpiderMain()
    obj_spider.crawlMain(root_url)
    # 此方法未完善
    # obj_spider.crawlBaseInfo()
    # obj_spider.crawlBaike()
