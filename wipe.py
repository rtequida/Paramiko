import paramiko
import sys
import time
from tkinter import *
from tkinter.font import *

COLOR = "gray5"

def main():
    root = Tk()
    root.config(bg = COLOR)

    nbytes = 4096
    hostname = ""
    port = 22
    password = ""
    first = 17
    last = 23
    run = 0

    root.mainloop()

    if run != 0:
        for i in range(first, last + 1):
            print ("Working on port " + str(i))
            username = "netadmin:port" + str(i)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(hostname, port = port, username = username, password = password)
            except paramiko.ssh_exception.AuthenticationException:
                print ("Couldn't connect")
                continue
            except:
                print ("Unknown Error")
                continue

            shell = ssh.invoke_shell()
            time.sleep(3)
            shell.send("\r\n")
            time.sleep(3)
            shell.send("***Enter user name here***\n")
            time.sleep(.5)
            shell.send("***Enter password here***\n")
            time.sleep(.5)
            shell.send("en\n")
            time.sleep(.5)
            shell.send("***Enter password here***\n")
            time.sleep(.5)
            print ("Destroying Data!!!")
            shell.send("write erase\n")
            time.sleep(.5)
            shell.send("\r\n")
            time.sleep(3)
            shell.send("delete flash:vlan.dat\n")
            time.sleep(.5)
            shell.send("\r\n")
            time.sleep(.5)
            shell.send("\r\n")
            time.sleep(.5)
            shell.send("reload\n")
            time.sleep(.5)
            shell.send("\r\n")
            time.sleep(.5)
            shell.send("no\n")
            time.sleep(.5)
            shell.send("\r\n")
            ssh.close()
            shell.close()

main()
