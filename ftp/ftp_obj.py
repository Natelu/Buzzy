# -*- coding: UTF-8 -*-

import client
import ftplib
import os


class FtpObj(object):
    def __init__(self, host_name, user_name='', password=''):
        self.host = host_name
        self.user = user_name
        self.password = password
        self.ftp = self.get_conn()

    def get_conn(self):
        try:
            print('start connecting to the ftp server %s...' % (self.host))
            ftp = ftplib.FTP(self.host)  # 实例化FTP对象
            ftp.connect(host=self.host, port=21)
            print('start logging to the ftp server with user %s...' % (self.user))
            ftp.login(self.user, self.password)  # 登录
            print('successfully logging the ftp server!') 
        except Exception as e:
            print(e)
            # ftp = None
        return ftp

    def download(self, file_name, remote_path=None, local_path=None):
        file_local = open(local_path + os.sep + file_name if local_path else file_name, 'wb')
        file_remote = remote_path + os.sep + file_name if remote_path else file_name
        bufferz_size = 1024
        self.ftp.retrbinary('RETR %s' % file_remote, file_local.write, bufferz_size)
        file_local.close()
        print('successfully download')
        
    def upload(self, file_name, local_path=None, remote_path=None):
        file_name = local_path + os.sep + file_name if local_path else file_name
        # client.encry_file(file_name)
        file_local = open(file_name, 'rb')
        file_remote = remote_path + os.sep + file_name if remote_path else file_name
        buffer_size = 1024
        self.ftp.storbinary('STOR ' + file_remote, file_local, buffer_size)
        file_local.close()
        print('successfully upload')


if __name__ == '__main__':
    host = '62.234.108.65'  # 凯哥
    # host = '95.169.30.124'
    username = 'ftp_user04'
    password = 'user04@ftp'
    remote_file = 'test.txt'
    local_file = 'XiaoHongShu.zip'
    ftp = FtpObj(host, username, password)
    if ftp:
        ftp.download(remote_file)
        ftp.upload(local_file)
        ftp.ftp.close()