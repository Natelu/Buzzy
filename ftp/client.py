# -*- coding: UTF-8 -*-

import base
import ftp_obj
import requests
import sys
from security import decrypt_file


def request(filename, action_type):
    url = 'http://%s:%s?filename=%s&type=%s' % (base.transfer['host'], base.transfer['http_port'], filename,action_type)
    # url = base.transfer['host'] + ':' + base.transfer['http_port'] + '?filename=%s&tyle=%s' % (filename, action_type)
    # print(url)
    req = requests.get(url)
    res = req.text
    return res


'''
    上传部分，上传至中转服务器，并给中转服务器发送信号2；
    下载部分，给中转服务器发送信号1，然后开始ftp下载。
'''


def upload_local(filename):
    machine = base.transfer
    # encry_file(filename)
    ftp = ftp_obj.FtpObj(machine['host'], machine['user'], machine['passwd'])
    ftp.upload(filename)  # upload to the transfer machine
    res = request(filename, base.action['upload'])  # send uploading signal to server to do the next job
    print(res)


def down_load(filename):
    machine = base.target
    ftp = ftp_obj.FtpObj(machine['host'], machine['user'], machine['passwd'])
    res = request(filename, base.action['download'])
    print(res)
    if res == 'the file has successfully download to the proxy server.':
        ftp.download(filename)
        decrypt_file(filename)


if __name__ == '__main__':
    file_name = sys.argv[2]
    action = int(sys.argv[1])   # 1下载， 2上传
    if action == 1:
        down_load(file_name)
    elif action == 2:
        upload_local(file_name)
    else:
        print('wrong action number!')