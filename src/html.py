# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import sys
from lxml import etree
from io import StringIO, BytesIO
import json
from Logger import Log

logger = Log.getLogger(__file__)


class Singleton(object):
    # __call__ makes the class can be use like this:
    # e.g
    # x=Singleton(args)
    #     def __call__(self, *args, **kwargs):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class HtmlParser():

    def __init__(self,name):
        self.name = name

    def parse(self, html):
        pass

class IPEntity:
    ip = ''
    port = ''
    anonymous = ''
    procotol = ''
    location = ''

def create_ip_entity(ip,port,anonymous,procotol,location):
    entity = IPEntity()
    entity.ip = ip
    entity.port = port
    entity.anonymous = anonymous
    entity.procotol = procotol
    entity.location = location
    return entity


class ChongDaiLiHtmlParser(HtmlParser):
    def parse(self, html):
        if html is None: return []
        tree = etree.parse(StringIO(html),etree.HTMLParser())
        tr = tree.xpath('//tbody/tr')
        results = []
        for t in tr:
            tds = t.xpath('td')
            ip = tds[0].text
            port = tds[1].text
            anonymous = tds[2].text
            procotol = tds[3].text
            location = tds[5].text


            entity = IPEntity()
            entity.ip = ip
            entity.port = port
            entity.anonymous = anonymous
            entity.procotol = procotol
            entity.location = location

            logger.debug('获取代理：%s %s %s %s %s',ip,port,anonymous,procotol,location)
            results.append(entity)
        return results

class XiCiDaiLiHtmlParser(HtmlParser):

    """
    西刺代理
    url：http://www.xicidaili.com/wn/

    有一个奇怪的问题，浏览器和wget得到的网页结构不一样
    """


    def parse(self, html):
        if html is None: return []

        logger.debug('正在解析西刺代理获取免费代理...')
        tree = etree.parse(StringIO(html),etree.HTMLParser())
        tr = tree.xpath('//table/tr')
        result = []
        for t in tr:
            if t is None: continue
            tds = t.xpath('td')
            if tds is None or len(tds) == 0: continue

            ip = tds[1].text
            port = tds[2].text
            anonymous = tds[4].text
            procotol = tds[5].text
            location = tds[9].text

            logger.debug('获取代理：%s %s %s %s %s',ip,port,anonymous,procotol,location)
            result.append(create_ip_entity(ip,port,anonymous,procotol,location))
        return result


class KuaiDaiLiHtmlParser(HtmlParser):
    """
    快代理
    url: https://www.kuaidaili.com/free/inha/1/

    分页网页，为保证有一定数量的ip，需要多爬几页

    """
    def parse(self, html):
        if html is None or html == '': return []
        tree = etree.parse(StringIO(html),etree.HTMLParser())
        logger.debug('正在解析快代理获取免费ip')
        trs = tree.xpath('//table/tbody/tr')
        result = []

        for tr in trs:
            if tr is None or '' == tr:continue
            tds = tr.xpath('td')

            ip = tds[0].text
            port = tds[1].text
            anonymous = tds[2].text
            procotol = tds[3].text
            location = tds[4].text

            logger.debug('获取代理：%s %s %s %s %s',ip,port,anonymous,procotol,location)
            result.append(create_ip_entity(ip,port,anonymous,procotol,location))
        return result

        pass


class XunDaiLiHtmlParser(HtmlParser):

    def parse(self, html):

        if html is None or '' == html: return []
        tree = etree.parse(StringIO(html),etree.HTMLParser())
        logger.debug('正在解析xun代理获取免费ip')
        trs = tree.xpath('//table/tbody/tr')
        result = []
        for tr in trs:
            if tr is None or '' == tr: continue
            tds = tr.xpath('td')

            ip = tds[0].xpath('div')[0].text
            port = tds[1].xpath('div')[0].text
            anonymous = tds[2].xpath('div/span')[0].text
            procotol = tds[3].xpath('div/span')[0].text
            location = tds[4].xpath('div')[0].text

            ip = str(ip).strip()
            port = str(port).strip()
            anonymous = str(anonymous).strip()
            procotol = str(procotol).strip()
            location = str(location).strip()

            logger.debug('获取代理：%s %s %s %s %s',ip,port,anonymous,procotol,location)
            result.append(create_ip_entity(ip,port,anonymous,procotol,location))
        return result
        pass

class XunDaiLiJsonParser(HtmlParser):

    def parse(self,json_str):
        if json_str is None or '' == json_str: return []
        logger.debug('正在解析Xun代理获取买费ip')
        ip_json = json.loads(json_str)
        ip_result =  ip_json['RESULT']
        if ip_result is None : return []
        result = []
        for ip_entity in ip_result['rows']:
            ip = ip_entity['ip']
            port = ip_entity['port']
            anonymous = ip_entity['anony']
            procotol = ip_entity['type']
            location = ip_entity['position']

            logger.debug('获取代理：%s %s %s %s %s',ip,port,anonymous,procotol,location)
            result.append(create_ip_entity(ip,port,anonymous,procotol,location))

        return result

if __name__ == '__main__':

    #chong_html_path = '/home/eason/workspace/python/proxy_pool/test/conf/xundaili.html';
    chong_html_path = 'index.html';
    html_content = open(chong_html_path, encoding='utf8')

    html_str = ''
    for line in html_content.readlines():
        html_str = html_str + str(line)
    #parser = XiCiDaiLiHtmlParser('C')
    parser = KuaiDaiLiHtmlParser('C')
    #parser = XunDaiLiHtmlParser('C')
    print(parser.parse(html_str))

