import matlab
import matlab.engine

import os
import paramiko

#def add_folders_to_path(eng, folder):
 #   eng.addpath(folder)
  #  for subdir, dirs, files in os.walk(folder):
   #     for dir in dirs:
    #        path = os.path.join(subdir, dir)
     #       eng.addpath(path)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 替换为您的服务器详情
hostname = '172.27.81.96'
username = 'user'
password = 'qaz@123'  # 或使用密钥认证

ssh.connect(hostname, username=username, password=password)
cmd = 'rm -rf /home/user/Verilog_hdlsrc'
stdin, stdout, stderr = ssh.exec_command(cmd)
error = stderr.read().decode('utf-8')

eng = matlab.engine.start_matlab()
folder_path = 'D:\slsf_randgen\slsf'# your slsf adress
#add_path_cmd = 'addpath(genpath('+folder_path+')'
#add_folders_to_path(eng, folder_path)
eng.addpath('D:\slsf_randgen\slsf')
eng.cd('D:\slsf_randgen\slsf')
eng.run('addpath_GUIDANCE.m', nargout=0)
eng.run('Hdl_generation.m', nargout=0)

Save_name = eng.workspace['stmp']
print(Save_name)
print('execute ssh remote power shell')



cmd = 'mkdir /doc/xzh/resamplesource/'+Save_name
stdin, stdout, stderr = ssh.exec_command(cmd)


cmd = 'cp -r /home/user/Verilog_hdlsrc /doc/xzh/resamplesource/'+Save_name+'/Verilog_hdlsrc'
stdin, stdout, stderr = ssh.exec_command(cmd)

# 获取命令的输出
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')

if error:
    print("Error:", error)
else:
    print("Output:", output)

cmd = 'cd /doc/xzh \n'+'/home/user/anaconda3/envs/xzh/bin/python3.9 /doc/xzh/test_main.py'
stdin, stdout, stderr = ssh.exec_command(cmd)

# 获取命令的输出
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')

if error:
    print("Error:", error)
else:
    print("Output:", output)
