#/bin/python
#coding=utf-8


import os 
from os.path import *


LOG_FILE = "files_dect.pkl"
CONFIG = {
    "name": "My Server",
    "host": "10.124.142.187",
    "protocol": "sftp",
    "port": 22,
    "username": "root",
    "remote_prefix": "/root/work/go/src/github.com/mesosphere/mesos-framework-tutorial",
    "uploadOnSave": True,
    "scan_sep": 2, # time interval between every continuous scaning.
    "scp_ignores": [LOG_FILE, '.git', '.vscode']
}
# LOG_FILE = "files_dect.pkl"

def extract_path(uri):
    lis = uri.split('/')
    lis = lis[0:len(lis) - 1]
    return '/'.join(lis)

# uplaod file to remote_server via scp service.
def upload(file_path, user, host, local_prefix, remote_prefix):
    '''
        本地路径：file_path == local_path 
        远程路径: remote_prefix + (local_path - local_prefix)
        '''
    remote_path = remote_prefix + file_path.replace(local_prefix, '')
    # print("remote_path == {}".format(remote_path))
    # print("after_extra == {}".format(extract_path(remote_path)))
    # print("remote_prefix {}".format((remote_path)))
    cmd = 'scp {file_path} {user}@{host}:{remote_path}'.format(file_path=file_path, user=user, host=host, remote_path=extract_path(remote_path))
    try:
        print(cmd)
        res = os.system(cmd)
        print("Success : {} upload success! ".format(file_path))
    except Exception as e:
        print(e)
        print("Error: {} upload failed! ".format(file_path))
    return

# walk the whole project to detect the changed files.
def walk(dict_file_description, local_path, local_prefix, user, host, remote_prefix):
    lis_file = os.listdir(local_path)
    # print('local_path: {} --- {}'.format(local_path, lis_file))
    for f in lis_file:
        if f in CONFIG['scp_ignores']:
            continue
        f = os.path.join(local_path, f) 
        if isfile(f):
            # print(f)
            file_name = os.path.abspath(f)
            file_mtime = os.path.getmtime(file_name)
            simple_name = file_name.replace(local_prefix, '')
            if simple_name not in dict_file_description.keys() or dict_file_description[simple_name] != file_mtime:
                # print(file_description)
                upload(file_name, user, host, local_prefix, remote_prefix)
                dict_file_description[simple_name] = file_mtime
        elif os.path.isdir(f):
            # print("###{}  has {};".format(f, os.listdir(f)))
            walk(dict_file_description, f, local_prefix, user, host, remote_prefix) 
        # else:
        #     print("folder ----- {}".format(f))

if __name__=="__main__":
    import pickle
    import time
    dect_file_name = "files_dect.pkl"
    local_path = abspath(dirname(__file__))
    # local_prefix = os.path.abspath("../") 
    local_prefix = local_path
    if not os.path.exists(dect_file_name):
        pickle.dump({}, open(dect_file_name, 'wb')) 
    # run walk every x seconds
    i = 1
    while True:
        file_description = pickle.load(open(dect_file_name, 'rb'))
        print('SCAN ITERS NUMBER..{} ...:'.format(i))
        walk(file_description, local_path, local_prefix, user=CONFIG['username'], host=CONFIG['host'], remote_prefix=CONFIG['remote_prefix'])
        pickle.dump(file_description, open(dect_file_name, 'wb'))
        time.sleep(CONFIG['scan_sep']) 
        i += 1 
