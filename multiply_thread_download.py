import requests
import os
import time
import math
import numpy as np

from threading import Thread
from time import sleep

'''
#data struct of download block
block_no ： {0,1,2,...} block序号
block_start ：block 开始位置
block_end ：block 结束位置
block_status {0,1} ：block状态 0=未下载， 1=已下载
block_content : byte 下载内容（二进制）
'''

#my_url = 'http://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png'
#filename = 'n.png'
my_url = 'http://mirrors.aliyun.com/pypi/packages/81/87/0c8592b31a6e19106699740f4a5ff33d60d0f365363168cf319d0fbe4950/pandas-1.3.0-cp37-cp37m-win_amd64.whl'
filename = 'n.whl'
#block_size = 4*1024
# the number of thread
thread_count = 4

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

# return the downlad file size, return 0 if error
def get_file_size(url):
    response = requests.head(url, verify=False)
    
    #except process，return file_size = 0 if error
    file_size = int(response.headers['Content-Length'])
    
    return file_size

# initial the blocks list structure
def block_initialization(file_size, thread_count=1):
    blocks = []
    block_no = 0
    start = 0
    end = -1
    block_content = ''
    
    block_size = file_size // thread_count
    
    while end < file_size -1:
        start = end +1
        end = start + block_size -1
        if end > file_size:
            end = file_size
        blocks.append({'block_num':block_no, 'start':start, 'end':end, 'status':0, 'block_content':block_content})
        block_no += 1
    
    return blocks

# download the data of each block
def download_block(url_name, start, end):
    headers = {"Range":"bytes="+str(start)+"-"+str(end)+""}
    res = requests.get(url_name, headers=headers)
    
    return res.content

# if the block data download or not
def is_block_downloaded(blocks, block_num):
    return blocks[block_num]['status']

# update the blocks if data downloaded.
def update_blocks(blocks, block_num, block_content):
    blocks[block_num]['status'] = 1
    blocks[block_num]['block_content'] = block_content
    
    return blocks
  
# the main function to download file
def download_file(url_name, blocks):
    threads = []
    for num in range(len(blocks)):
        block_no = blocks[num]['block_num']
        start = blocks[num]['start']
        end = blocks[num]['end']
        status = blocks[num]['status']
                
        if is_block_downloaded(blocks, block_no) == 0:
          # create thread to download block data
            thread = MyThread(download_block, args=(my_url, start, end))
            thread.start()
            threads.append(thread)
    # waiting all thread return
    for t in threads:
        t.join()
    # update download data to blocks
    for i in range(len(threads)):
        update_blocks(blocks, i, threads[i].get_result())
    
    return blocks

start_time = time.perf_counter()

file_size = get_file_size(my_url)
print(file_size)
blocks = block_initialization(file_size, thread_count)
download_blocks = download_file(my_url, blocks)
# write data to file
for i in range(len(download_blocks)):
    with open(filename,'ab+') as f:
        f.write(download_blocks[i]['block_content'])
        
print('finish to write')

end_time = time.perf_counter()
print(f'finished in {round(end_time-start_time, 2)} seconds')
