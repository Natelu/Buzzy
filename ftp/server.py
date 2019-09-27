# -*- coding: UTF-8 -*-
import base
import BaseHTTPServer
import CGIHTTPServer
import SimpleHTTPServer
import SocketServer
import urllib
import io
import shutil
import sys
from security import encry_file
import ftp_obj


#定义数据处理模块--此部分可放于外部引用文件
class dataHandler(object):
    # #接口分发
    # def __int__(self):
    #     self.ftp = ftp_obj.FtpObj('95.169.30.124', 'ftp_user02', 'user02@ftp').get_conn()

    def run(self, path, args):
        filename = str(args).split('&')[0].split('=')[1]
        typenum = int(str(args).split('&')[1].split('=')[1])
        print(filename, typenum)
        result = ''
        cloud_machine = base.target
        ftp = ftp_obj.FtpObj(cloud_machine['host'], cloud_machine['user'], cloud_machine['passwd'])
        try:
            if typenum == 1: # 下载选项
                ftp.download(filename)
                result = 'the file has successfully download to the proxy server.'
            else:
                encry_file(filename)
                ftp.upload(filename)
                result = 'the file has successfully upload to the target server.'
        except Exception as e:
            result = str(e)
        return result


# 服务环境搭建
class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        mpath,margs=urllib.splitquery(self.path) # ?分割
        if margs==None:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.do_action(mpath, margs)

    def do_POST(self):
        mpath,margs=urllib.splitquery(self.path)
        datas = self.rfile.read(int(self.headers['content-length']))
        self.do_action(mpath, datas)

    #请求处理方法
    def do_action(self, path, args):
        dh = dataHandler()
        result = dh.run(path, args)
        self.outputtxt(result)
        print(path, args)
    #数据返回到前台

    def outputtxt(self, content):
        #指定返回编码
        enc = "UTF-8"
        content = content.encode(enc)
        f = io.BytesIO()
        f.write(content)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)
        #SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


if __name__ == '__main__':
    #web服务主程序
    PORT = int(sys.argv[1])
    print(PORT)
    httpd = SocketServer.TCPServer(("", PORT), ServerHandler)
    print("serving at port", PORT)
    httpd.serve_forever()