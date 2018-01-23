#!/usr/local/bin/python3.6

__author__ = 'XiaoMiZhou'

__date__ = '2018/1/26'

import re
import sys
import json

from db import RedisClient

from bottle import route,run,get,post,response
import configparser

config = configparser.ConfigParser()
config.read('conf/ipool.cnf')

redis_host = config['redis']['host']
redis_username = config['redis']['username']
redis_password = config['redis']['password']
redis_port= config['redis']['port']
redis_db= config['redis']['database']

redis =  RedisClient(host=redis_host, port=redis_port, username=redis_username, password=redis_password, db=redis_db)


server_host = config['server']['host']
server_port = config['server']['port']

"""

"""

resp_templete = {
        'code':'',
        'message':'',
        'results':[]
        }

def normal_resp(code,content):
    resp_templete['results'] = content
    resp_templete['code'] = content
    return json.dumps(resp_templete)

def invalid_resp(code,message):
    resp_templete['code'] = code
    resp_templete['message'] = message
    return json.dumps(resp_templete)


def define_response():
    response.content_type = 'application/json;charset=UTF-8'


@get('/ipool/get/<procotol>/<anonymous>/<amount>')
def get_ip(procotol,anonymous,amount):

    define_response()
    ips = redis.get(procotol,anonymous,int(amount))
    if ips is None or 0 == len(ips):
        return invalid_resp(1,'ipool没有ip了，稍后再来吧！！')

    results = [entity.decode('utf-8') for entity in ips]
    return normal_resp(0,results)



def main():
    pass
if __name__ == '__main__':
    main()
    run(host=server_host,port=server_port)
    pass


