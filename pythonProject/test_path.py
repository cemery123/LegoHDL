
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 替换为您的服务器详情
hostname = '172.27.81.96'
username = 'user'
password = 'qaz@123'  # 或使用密钥认证

ssh.connect(hostname, username=username, password=password)

cmd = 'source ~/.bashrc; echo $PATH;export PATH=$PATH:/doc/Xilinx/Vivado/2023.2/bin; echo $PATH;source ~/.bashrc'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')
if error:
    print("Error:", error)
else:
    print("Output:", output)

cmd = '/doc/Xilinx/Vivado/2023.2/bin/vivado -mode batch -source /doc/xzh/resamplesource/2024-01-29-11-29-59/Verilog_hdlsrc/sampleModel1702_sub/vivado_sim.tcl'
stdin, stdout, stderr = ssh.exec_command(cmd)
output = stdout.read().decode('utf-8')
error = stderr.read().decode('utf-8')

if error:
    print("Error:", error)
else:
    print("Output:", output)