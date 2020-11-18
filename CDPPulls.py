import paramiko
import sys
import time

nbytes = 4096
hostname = ""
port = 22
username = "***Enter username here***"
password = "***Enter password here***"
command = "ls"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, port = port, username = username, password = password)
time.sleep(2)
print ("here")

stdin, stdout, stderr = ssh.exec_command("sh inven")
output = stdout.readlines()
for line in output:
    print (line)
