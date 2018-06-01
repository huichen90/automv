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



