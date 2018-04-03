# -*- coding:utf-8 -*-
import uuid
import time

import pymysql as pymysql


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
                    sql = "insert into `singer`(`id`,`href`,`name`,`site`,`time`) values(%s,%s,%s,%s,%s)"
                    print(data['name'])
                    cursor.execute(sql, (str(data['id']), data['href'], data['name'], data['site'], str(data['time'])))
                    connection.commit()
                    print("    -保存成功~")
        finally:
            connection.close()

    def listSinger(self):
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                sql = "select `id`,`href`,`name`,`site`,`time` from `singer`"
                print(sql+":"+sql)
                cursor.execute(sql)
                datas = cursor.fetchmany(size=6000)
            connection.commit()
            return datas

        finally:
            connection.close()

    def saveBaseInfo(self, singer_id, datas):
        # TODO
        pass

    def saveBaike(self, singer_id, singer_baike_url, html_doc, itemDatas):
        connection = pymysql.connect(**self.config)
        if itemDatas is None:
            return
        try:
            with connection.cursor() as cursor:
                baike_id = str(uuid.uuid1())
                sql = "insert into `baike`(`id`, `singer_id`, `time`, `href`, `html_doc`) values(%s,%s,%s,%s,%s)"
                cursor.execute(sql, (baike_id, singer_id, str(time.time()), singer_baike_url,
                                     str(html_doc.decode(encoding='UTF-8'))))
                connection.commit()
                for item in itemDatas:
                    sql = "insert into `baike_item`(`id`,`baike_id`,`order`,`name`,`value`) values(%s,%s,%s,%s,%s)"
                    cursor.execute(sql, (str(uuid.uuid1()), baike_id, item['order'], item['name'], item['value']))
                    connection.commit()
        finally:
            connection.close()
