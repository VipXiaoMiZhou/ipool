# -*- coding: utf-8 -*-
#!/usr/local/bin/python3.6

__author__ = 'XiaoMiZhou'

__date__ = '2018/1/25'

import time
from threading import Thread

import tools
from Logger import Log
from db import RedisClient
from html import KuaiDaiLiHtmlParser
from html import XiCiDaiLiHtmlParser
from html import XunDaiLiJsonParser

import configparser

config = configparser.ConfigParser()
config.read('conf/ipool.cnf')

host = config['redis']['host']
username = config['redis']['username']
password = config['redis']['password']
port = config['redis']['port']
db = config['redis']['database']

redis = RedisClient(host=host, port=port, username=username, password=password, db=db)

logger = Log.getLogger(__file__)

# chong = ChongDaiLiHtmlParser('A')
xici = XiCiDaiLiHtmlParser('xici_daili')
kuai = KuaiDaiLiHtmlParser('kuai_daili')
xun = XunDaiLiJsonParser('xun_daili')

urls = {xici.name: 'http://www.xicidaili.com/nt/', kuai.name: 'https://www.kuaidaili.com/free/',
        xun.name: 'http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10'}
parsers = {xici.name: xici, kuai.name: kuai, xun.name: xun}


def do_crawl(url, proxy=None):
    """
    抓取网页
    :param url: 待抓取网页url
    :param proxy: 代理
    :return: 网页
    """
    if url is None or url == '': return
    logger.info('开始抓取网页:%s', url)
    return tools.html_downloader(url, proxy)


def do_start(name, url):
    if name is None or name == '': return
    if url is None or url == '': return

    # 下载网页
    html_str = do_crawl(url, None)

    p = parsers[name]
    if p is None:
        logger.debug('未找到%s对应的网页解析器', name)
        return

    logger.info('开始解析网页', p.name)

    ips = p.parse(html_str)

    for ip in ips:
        if ip is None: continue

        host = ip.ip
        port = ip.port
        anonymous = ip.anonymous
        procotol = ip.procotol

        https_proxy = str('https').lower() + '://' + host + ':' + str(port)
        http_proxy = str('http').lower() + '://' + host + ':' + str(port)

        if tools.check_liveness(https_proxy):
            logger.info('https代理%s可用', https_proxy)
            redis.put('https', '1', host, port)

        if tools.check_liveness(http_proxy):
            logger.info('http代理%s可用', http_proxy)
            redis.put('http', '1', host, port)


def main():
    while 1:
        threads = [Thread(target=do_start, args=(name, url)) for name, url in urls.items()]
        srt = [th.start() for th in threads]
        stp = [th.join() for th in threads]
        print('over')
        time.sleep(200)

    pass

if __name__ == '__main__':
    main()