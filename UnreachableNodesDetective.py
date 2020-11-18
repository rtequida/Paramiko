import paramiko
import sys
import time
import xlrd
import csv
import subprocess
import os

def main():
    loc = ("UnreachableDevices.xlsx")
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    device_IPs = getData(sheet)
    info = pingable(device_IPs)
    info = conclusion = findAnswers(info)
    for key in info:
        print(key, ":", info[key])

def getData(sheet):
    data = []
    for i in range(sheet.nrows):
        data.append(sheet.cell_value(i, 0))
    return data

def pingable(ips):
    info = {}
    nos = 0
    yes = 0
    length = len(ips)
    count = 0
    with open(os.devnull, "wb") as limbo:
        for ip in ips:
            count += 1
            result = subprocess.Popen(["ping", "-n", "1", "-w", "200", ip], stdout=limbo, stderr=limbo).wait()
            if result:
                print(ip, "\t: failed", " (", count, "/", length, ")")
                info[ip] = "NO"
                nos += 1
            else:
                print(ip, "\t: passed", " (", count, "/", length, ")")
                info[ip] = "YES"
                yes += 1
    print("Failed: ", nos, "\nPassed: ", yes)
    return info

def findAnswers(info):
    nbytes = 4096
    port = 22
    username = ""
    password = ""
    command = "ls"
    output = ""
    for ip in info:
        if info[ip] == "YES":
            hostname = ip
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print("Testing: ", hostname)
            try:
                ssh.connect(hostname, port = port, username = username, password = password)
            except paramiko.ssh_exception.AuthenticationException:
                print("Could not authenticate to host " + hostname)
                info[ip] = "Could not authenticate to host"
                continue
            except paramiko.ssh_exception.NoValidConnectionsError:
                print("Could not connect to host " + hostname)
                info[ip] = "Could not connect to host"
                continue
            except paramiko.ssh_exception.SSHException:
                print("Failures in SSH2 protocol")
                info[ip] = "Failed to establish SSH connection"
                continue
            except:
                print("Unknown Error")
                info[ip] = "Unknown Error"
                continue
            time.sleep(2)
            print ("Successfully connceted to " + hostname)
            info[ip] = "Success"
            ssh.close()
    return info
main()
