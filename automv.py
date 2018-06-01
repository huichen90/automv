# -*- coding: utf-8 -*-

import datetime

import paramiko
import os

def remote_scp(host, port, remote_dir, local_dir, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, port=port, username=username, password=password, timeout=10)
        sftp = client.open_sftp()
        keywords = sftp.listdir(remote_dir)
        for keyword in keywords:                                              # keywords层
            dts= sftp.listdir(remote_dir+'/'+keyword)
            for dt in dts:                                                    #datatime层
                try:
                    f = open(local_dir+'/'+keyword+'/'+dt)
                    f.close()
                except IOError:
                    try:
                        os.makedirs(local_dir+'/'+keyword+'/'+dt)
                    except FileExistsError:
                        pass
                files = sftp.listdir(remote_dir+'/'+keyword+'/'+dt)
                for f in files:                                                 #file层
                    print("********************************")
                    sftp.get(remote_dir+'/'+keyword+'/'+dt + '/' + f , os.path.join(local_dir+'/'+keyword+'/'+dt, f))
                    # sftp.put('{{localhost_file_path}}', '{{target_location_filepath}}')
                    print('Download file  %s success %s ' % (f,datetime.datetime.now()))
                    print("********************************")
                    sftp.remove(remote_dir+'/'+keyword+'/'+dt + '/' + f)
                    print('Delete %s/%s/%s success' % (keyword,dt,f))
                sftp.rmdir(remote_dir+'/'+keyword+'/'+dt)
                print('Delete %s/%s success' % (keyword,dt))
            sftp.rmdir(remote_dir+'/'+keyword)
            print('Delete %s success' % keyword)
        print('Download files all success')
        sftp.close()
    except Exception:
        print("connect error!")
if __name__ == '__main__':

    host = ''   # 目标主机host
    port = 22   # ssh协议端口
    username = 'root'  # 登录的User
    password = 'password'
    remote_dir = "/root/videos"
    local_dir = '/home/videos'
    remote_scp(host=host,port=port,username=username,password=password,remote_dir=remote_dir,local_dir=local_dir)





#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import paramiko, datetime, os
#
# host_ip = '47.91.236.20'
# username1 = '***'
# password1 = '****'
# port = 22
# local_dir = 'd:/aaa'
# remote_dir = '/home/temp/Templates'
# try:
#     t = paramiko.Transport(host_ip, port)
#     t.connect(username=username1, password=password1)
#     sftp = paramiko.SFTPClient.from_transport(t)
#     files = os.listdir(local_dir)  # 上传多个文件
#     # files = sftp.listdir(remote_dir)  # 下载多个文件
#     for f in files:
#         print ''
#         print '#########################################'
#         print 'Beginning to download file  from %s  %s ' % (host_ip, datetime.datetime.now())
#         print 'Downloading file:', (remote_dir + '/' + f)
#         # sftp.get(remote_dir + '/' + f, os.path.join(local_dir, f))  # 下载多个文件
#         sftp.put(os.path.join(local_dir, f), remote_dir + '/' + f)  # 上传多个文件
#         print 'Download file success %s ' % datetime.datetime.now()
#         print ''
#         print '##########################################'
#     t.close()
# except Exception:
#     print "connect error!"