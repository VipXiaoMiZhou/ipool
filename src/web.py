# -*- coding: utf-8 -*-
#!/usr/local/bin/python3.6

__author__ = 'XiaoMiZhou'

__date__ = '2018/1/26'

import configparser
import json
from bottle import run, get, response

from db import RedisClient

config = configparser.ConfigParser()
config.read('conf/ipool.cnf')

redis_host = config['redis']['host']
redis_username = config['redis']['username']
redis_password = config['redis']['password']
redis_port = config['redis']['port']
redis_db = config['redis']['database']

redis = RedisClient(host=redis_host, port=redis_port, username=redis_username, password=redis_password, db=redis_db)

server_host = config['server']['host']
server_port = config['server']['port']

"""

"""

resp_templete = {
    'code': '',
    'message': '',
    'results': []
}


def resp(code, message, results):
    resp_templete['results'] = results
    resp_templete['code'] = code
    resp_templete['message'] = message
    return json.dumps(resp_templete)


def define_response():
    response.content_type = 'application/json;charset=UTF-8'


@get('/ipool/get/<procotol>/<anonymous>/<amount>')
def get_ip(procotol, anonymous, amount):
    define_response()
    ips = redis.get(procotol, anonymous, int(amount))
    if ips is None or 0 == len(ips):
        return resp(1, 'ipool没有ip了，稍后再来吧！！', [])

    results = [entity.decode('utf-8') for entity in ips]
    return resp(0, '', results)


def main():
    run(host=server_host, port=server_port)
    pass


if __name__ == '__main__':
    main()
