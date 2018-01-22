# -*- coding: utf-8 -*-
# !/usr/bin/env python

from urllib import request
import multiprocessing
import time
import tools
import random
from threading import Thread
from Logger import Log
from threading import current_thread
import threading


from html import ChongDaiLiHtmlParser
from html import XiCiDaiLiHtmlParser
from html import KuaiDaiLiHtmlParser
from html import XunDaiLiHtmlParser
from html import XunDaiLiJsonParser


from db import RedisClient

host = 'localhost'
username = None
password = None
port=6379
db=0

redis =  RedisClient(host=host, port=port, username=username, password=password, db=db)

logger = Log.getLogger(__file__)

#chong = ChongDaiLiHtmlParser('A')
xici = XiCiDaiLiHtmlParser('xici_daili')
kuai = KuaiDaiLiHtmlParser('kuai_daili')
xun  = XunDaiLiJsonParser('xun_daili')

urls = {xici.name:'http://www.xicidaili.com/nt/',kuai.name:'https://www.kuaidaili.com/free/',xun.name:'http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10'}
parsers = {xici.name:xici,kuai.name:kuai,xun.name:xun}

def start(name,url):
    if name is None or name == '' : return
    if url is None or url == '' : return
    logger.info('开始下载网页:%s',url)
    html_str = tools.html_downloader(url,None)
    p = parsers[name]

    if p is None:
        logger.debug('未找到%s对应的网页解析器',name)
        return

    logger.info('%s开始解析网页',p.name)
    ips = p.parse(html_str)

    for ip in ips:
        if ip is None: continue

        host = ip.ip
        port = ip.port
        anonymous = ip.anonymous
        procotol = ip.procotol

        https_proxy = str('https').lower()+'://'+host+':'+str(port)
        http_proxy = str('http').lower()+'://'+host+':'+str(port)

        if tools.check_liveness(https_proxy):
            logger.info('https代理%s可用',https_proxy)
            redis.put('https','1',host,port)

        if tools.check_liveness(http_proxy):
            logger.info('http代理%s可用',http_proxy)
            redis.put('http','1',host,port)

if __name__=='__main__':

    while 1:
        threads = [Thread(target=start,args=(name,url)) for name,url in urls.items()]
        srt = [th.start() for th in threads]
        stp = [th.join() for th in threads]
        print('over')
        time.sleep(200)

