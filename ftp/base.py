# -*- coding: UTF-8 -*-

# 基本配置信息，包括服务器，各服务器上ftp账户信息


transfer = {
    'host': '62.234.108.65',  # 中转服务器
    'user': 'ftp_user04',       # ftp用户
    'passwd': 'user04@ftp',
    'http_port': '8001'
}

target = {
    'host': '95.169.30.124',  # 目标云服务器
    'user': 'ftp_user02',       # ftp用户
    'passwd': 'user02@ftp'
}

action = {
    'upload': 2,  # 上传文件
    'download': 1  # 文件下载
}

CRYPT_KEY = '1234567890000000'
CRYPT_LENGTH = 16