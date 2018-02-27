# -*- coding: utf-8 -*-
# !/usr/local/bin/python3.6

__author__ = 'XiaoMiZhou'

__date__ = '2018/2/27'

from Logger import Log
import task
import web
import os
import multiprocessing


# 配置文件检查
def init_cnf():
    pass


# 环境检查
def init_env():
    pass


def install_lib():
    pass


# 启动任务
def run_task():
    web_process = multiprocessing.Process(name='web', target=web.main)
    task_process = multiprocessing.Process(name='task', target=task.main)

    web_process.start()
    task_process.start()
    pass

if __name__ == "__main__":
    print('hahahhahah')
    pass