# -*- coding:utf-8 -*-
import uuid
import time

import pymysql as pymysql
from singer_spider.happyjuzi.juzi_const import const
import logging
logger = logging.getLogger()

class DbHelper(object):


    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'db': 'memo_spider',
        'charset': 'utf8'
    }

    # 检查是否已经抓取
    def selectPageURL(self, url):
        connection = pymysql.connect(**self.config)

        try:
            with connection.cursor() as cursor:
                sql = "select `id`,`href`,`time`, `status` from `juzi_pageurl` where href = %s limit 1"
                cursor.execute(sql, ( url['href']))
                return cursor.rowcount
        finally:
            connection.close()

    # 检查是否已经抓取
    def selectStarURL(self, url):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                sql = "select `id`, `name`, `href`, `time`, `status` from `juzi_starurl` where href = %s limit 1"
                cursor.execute(sql, ( url['href']))
                return cursor.rowcount
        finally:
            connection.close()


    def savePageURLs(self, datas):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                for data in datas:
                    if self.selectPageURL(data) != 0:
                        continue
                    sql = "insert into `juzi_pageurl`(`id`,`href`,`time`, `status`) values(%s,%s,%s,%s)"
                    cursor.execute(sql, (str(data['id']), data['href'], str(data['time']), const.INSERET_PAGE_STATUS))
                    connection.commit()
                    logger.info(data['href'] +" --保存成功~")
        finally:
            connection.close()

    def saveStarURLs(self, starUrls):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                for data in starUrls:
                    if self.selectStarURL(data) != 0:
                        #logger.info(data['name']+'的url已经被抓取~')
                        continue
                    sql = "insert into `juzi_starurl`(`id`,`name`,`href`,`time`, `status`) values(%s,%s,%s,%s,%s)"
                    cursor.execute(sql, (str(data['id']), data['name'], data['href'], str(data['time']), const.INSERET_STAR_STATUS))
                    connection.commit()
                    logger.info(data['name']+":"+data['href'] + " --保存成功~")
        finally:
            connection.close()

    def select10PageURL(self):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                sql = "select `id`,`href`,`time`, `status` from `juzi_pageurl` where status != %s limit 10"
                cursor.execute(sql, const.CRAWL_PAGEURL_SUCCESS)
                if cursor.rowcount == 0:
                    return None
                else:
                    return cursor.fetchall()
        finally:
            connection.close()

    #查询固定条数待抓取明星页面url
    def select10StarURL(self):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                sql = "select `id`,`href`,`name`, `time`, `status` from `juzi_starurl` where status = %s limit 10"
                cursor.execute(sql, const.SELECT_STAR_STATUS)
                if cursor.rowcount == 0:
                    return None
                else:
                    return cursor.fetchall()
        finally:
            connection.close()


    def updatePageUrlStatus(self, pageUrlId, status):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                sql = "update `juzi_pageurl` set `status` = %s where id = %s"
                logger.info("更新id是" + str(pageUrlId) + "的页面url抓取状态为" + str(status))
                cursor.execute(sql, (status, str(pageUrlId)))
                connection.commit()
                logger.info(pageUrlId + "--抓取状态更新~")
        finally:
            connection.close()

    def updateStarUrlStatus(self, starUrlId, status):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                sql = "update `juzi_starurl` set `status` = %s where id = %s"
                logger.info("更新id是" + str(starUrlId) + "的明星url抓取状态为" + str(status))
                cursor.execute(sql, (status, str(starUrlId)))
                connection.commit()
                logger.info(starUrlId + "--抓取状态更新~")
        finally:
            connection.close()




