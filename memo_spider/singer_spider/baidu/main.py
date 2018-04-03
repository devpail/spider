# -*- coding:utf-8 -*-

# 爬虫总调main函数
import urllib.parse

from singer_spider.baidu import db_helper, html_downloader
from singer_spider.baidu import html_parser


class SpiderMain(object):
    # 初始化方法
    def __init__(self):
        # 初始化下载器
        self.downloader = html_downloader.HtmlDownload()
        # 初始化解析器
        self.parser = html_parser.HtmlParser()
        # 初始化数据库存储
        self.dbHelper = db_helper.DbHelper()

    # 抓取歌手名字
    def crawlSinger(self, root_url):
        # 下载url页面html
        htmlCode = self.downloader.download(root_url)
        # print(htmlCode.decode('utf-8'))
        # 解析html代码
        datas = self.parser.parseSinger(htmlCode)
        print(datas)
        print(len(datas))
        # 存储到数据库中
        self.dbHelper.saveSinger(datas)

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

    # 抓取百科词条信息，主要为了抓取生日信息
    def crawlBaike(self):
        # 从数据库中取出所有的名字信息
        singers = self.dbHelper.listSinger()
        # print(len(singers))
        # 循环遍历 `id`,`href`,`happyjuzi`,`site`,`time`
        for singer in singers:
            try:
                # 下载百度音乐页面
                singer_baike_url = 'https://baike.baidu.com/item/' + urllib.parse.quote(singer[2])
                html_doc = self.downloader.download(singer_baike_url)
                # print(html_doc.decode(encoding='UTF-8'))
                # 抓取百科页面信息
                itemDatas = self.parser.parseBaike(html_doc)
                if itemDatas is None:
                    print(singer[2] + "-没有数据！")
                else:
                    # 存储抓取的数据
                    print(singer[2] + "-保存资料~")
                    self.dbHelper.saveBaike(singer[0], singer_baike_url, html_doc, itemDatas)
            except:
                print(singer[2] + ":crawl faild!")


if __name__ == "__main__":
    root_url = "http://music.baidu.com/artist"
    obj_spider = SpiderMain()
    # obj_spider.crawlSinger(root_url)
    # 此方法未完善
    # obj_spider.crawlBaseInfo()
    obj_spider.crawlBaike()
