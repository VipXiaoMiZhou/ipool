# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'XiaoMiZhou'

__date__ = '2018/1/24'

import redis


class DBClient(object):
    def __init__(self, host, username, password, port, db):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.db = db
        self.conn = self.connect()

    def connect(self):
        pass

    def get(self, protocol='1', anonymous='1', amount=1):
        """ get a proxy address from pool
        :param protocol:  1 http  2 https
        :param anonymous: 1 透明代理 2 匿名代理 3 高匿代理
        :param amount:    每次获取代理的数量
        :return: 两分钟以内live的代理 e.g [192.168.36.56:6542]
        """
        pass

    def put(self, protocol, anonymous, ip, port):
        """
        :param protocol:
        :param anonymous:
        :param ip:
        :param port:
        :return:
        """
        pass

    def delete(self):
        pass

    def get_pool_size(self, protocol, anonymous=1):
        pass

    def get_all(self):
        pass

    def clear_pool(self):
        pass

    pass


class RedisClient(DBClient):
    def connect(self):
        return redis.Redis(host=self.host, port=self.port, db=self.db, password=None)

    def clear_pool(self):
        self.conn.flushdb()

    def put(self, protocol, anonymous, ip, port):
        name = self._generate_name(protocol, anonymous)
        value = self._generate_value(ip, port)
        return self.conn.lpush(name, value)

    def get(self, protocol='1', anonymous='1', amount=1):
        name = self._generate_name(protocol, anonymous)
        result = []
        for i in range(0, amount):
            ip = self.conn.lpop(name)
            if None == ip: continue
            result.append(ip)
        return result

    def get_pool_size(self, protocol, anonymous=1):
        name = self._generate_name(protocol, anonymous)
        return self.conn.llen(name)

    def get_all(self):
        # TODO get all ip from pool
        pattern = self._generate_name('?', '?')
        keys = self.conn.keys(pattern)
        results = []

        # for key in keys:
        #     results.append(self.conn.)

    def _generate_name(self, protocol, anonymous=1):
        """
        name procotol:1 anonymous:1
        :param protocol:
        :param anonymous:
        :return:
        """
        return 'protocol:' + str(protocol) + ' anonymous:' + str(anonymous)

    def _generate_value(self, ip, port):
        return str(ip) + ':' + str(port)


class MysqlClient(DBClient):
    # TODO mysql client
    pass


class MongoClient(DBClient):
    # TODO monogo client
    pass


if __name__ == "__main__":
    r = RedisClient(host='localhost', port=6379, username=None, password=None, db=0)
    r.put(1, 23, 312, '192.168.56.14')
    r.put(1, 23, 312, '192.168.56.14')
    r.put(1, 23, 312, '192.168.56.14')

    # print(r.get_pool_size(1, 23))
    # print(r.get(protocol='1', amount=10, anonymous=23))
    print(r.get_pool_size(1, 23))
    print('yes')
