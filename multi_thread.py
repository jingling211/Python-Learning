# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 16:59:16 2021

@author: Z0064529
"""

import requests
from threading import Thread
from time import sleep
import os
import time

# 设置进程数
threadnum = 5

my_url = 'http://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png'
#my_url = 'http://mirrors.aliyun.com/pypi/packages/81/87/0c8592b31a6e19106699740f4a5ff33d60d0f365363168cf319d0fbe4950/pandas-1.3.0-cp37-cp37m-win_amd64.whl'
filename = 'n.png'
#filename = 'n.whl'

# thread class
class MyThread(Thread):
    def __init__(self, func, args):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

# file download fun
def file_download(url_name, start, end):
    headers = {"Range":"bytes="+str(start)+"-"+str(end)+""}
    res = requests.get(url_name, headers=headers)
    return res.content

# 计时器 开始
start_time = time.perf_counter()

response = requests.head(my_url)
# 获得下载文件大小
filesize = int(response.headers['Content-Length'])

step = filesize // threadnum
start = 0
end = -1

# 进程数组
threads = []
# 计算各段起始，结束位置， 创建进程，启动进程
while end < filesize -1:
    start = end +1
    end = start + step -1
    if end > filesize:
        end = filesize
    print('start:', start)
    print('end:', end)
    
    thread = MyThread(file_download,
                args=(my_url, start, end)
                )
    thread.start()
    threads.append(thread)

# join 进程
for t in threads:
    t.join()

# 下载内容数组
recs = []
# 合并下载内容
for i in range(len(threads)):
    recs.append(threads[i].get_result())

#print(recs[0])

# 将下载内容保持到文件
for i in range(len(recs)):
    with open(filename,'ab+') as f:
        f.write(recs[i])
        
print('finish to write')

# 计时器 结束
end_time = time.perf_counter()
# 打印计时结果
print(f'finished in {round(end_time-start_time, 2)} seconds')