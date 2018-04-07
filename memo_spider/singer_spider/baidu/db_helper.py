# -*- coding:utf-8 -*-
import uuid
import time
import pymysql as pymysql
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()
class DbHelper(object):
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'db': 'memo_spider',
        'charset': 'utf8'
    }
    def saveSinger(self, datas):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                for data in datas:
                    if self.getSingerByHref(data['href']) != 0:
                        logger.info(data['name']+'的url已经被抓取~')
                        continue
                    sql = "insert into `singer`(`id`,`href`,`name`,`site`,`time`) values(%s,%s,%s,%s,%s)"
                    cursor.execute(sql, (str(data['id']), data['href'], data['name'], data['site'], str(data['time'])))
                    connection.commit()
                    logger.info(data['name']+":"+data['href'] + "    -保存成功~")
        finally:
            connection.close()

    # 检查是否已经抓取
    def getSingerByHref(self, href):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                sql = "select `id`, `name`, `href`, `time`, `site`, `status` from `singer` where href = %s limit 1"
                cursor.execute(sql, (str(href)))
                return cursor.rowcount
        finally:
            connection.close()

    #获取10条未抓取成功的歌手
    def get10Singer(self):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                sql = "select  aa.id,aa.href,aa.name from singer aa LEFT JOIN baike bb on aa.id = bb.singer_id where bb.id is null limit 10"
                cursor.execute(sql)
                if cursor.rowcount == 0:
                    return None
                else:
                    return cursor.fetchall()
        finally:
            connection.close()

    def listSinger(self):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                sql = "select `id`,`href`,`name`,`site`,`time` from `singer`"
                logger.info(sql+":"+sql)
                cursor.execute(sql)
                datas = cursor.fetchmany(size=6000)
            connection.commit()
            return datas

        finally:
            connection.close()

    def saveBaseInfo(self, singer_id, datas):
        # TODO
        pass

    # 验证singer百科页面是否被抓取
    def getSingerBaike(self, href):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                sql = "select  aa.*  FROM baike aa LEFT JOIN singer bb ON aa.singer_id =bb.id where bb.href = %s "
                cursor.execute(sql, href)
                return cursor.rowcount
        finally:
            connection.close()

    def saveBaike(self, singer_id, singer_baike_url, soup, itemDatas):
        connection = pymysql.connect(**self.config)
        if itemDatas is None:
            return
        try:
            with connection.cursor() as cursor:
                baike_id = str(uuid.uuid1())
                sql = "insert into `baike`(`id`, `singer_id`, `time`, `href`, `html_doc`) values(%s,%s,%s,%s,%s)"
                cursor.execute(sql, (baike_id, singer_id, str(time.time()), singer_baike_url,
                                     str(soup)))
                connection.commit()
                for item in itemDatas:
                    sql = "insert into `baike_item`(`id`,`baike_id`,`order`,`name`,`value`) values(%s,%s,%s,%s,%s)"
                    cursor.execute(sql, (str(uuid.uuid1()), baike_id, item['order'], item['name'], item['value']))
                    connection.commit()
        finally:
            connection.close()
