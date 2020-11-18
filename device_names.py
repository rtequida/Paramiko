import paramiko
import sys
import time
import xlrd
import csv

def main():
    loc = ("All Switches.xlsx")
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    all_switches = getData(sheet)
    info = pullInfo(all_switches)
    info = parseInfo(info)
    writeData(info)

def pullInfo(all_switches):
    info = []
    nbytes = 4096
    port = 22
    username = ""
    password = ""
    command = "ls"
    output = ""
    for sw in all_switches:
        hostname = sw
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname, port = port, username = username, password = password)
        except paramiko.ssh_exception.AuthenticationException:
            print("Could not authenticate to host " + hostname)
            info.append("Couldn't connect to " + hostname)
            continue
        except paramiko.ssh_exception.NoValidConnectionsError:
            print("Could not connect to host " + hostname)
            info.append("Couldn't connect to " + hostname)
            continue
        except:
            print("Unknown Error")
            info.append("Couldn't connect to " + hostname)
            continue
        time.sleep(2)
        print ("Successfully connected to " + hostname)
        shell = ssh.invoke_shell()
        time.sleep(2)
        output = shell.recv(2000)
        shell.send("sh inven\n")
        time.sleep(2)
        if shell.recv_ready():
            output = shell.recv(1000)
            if "missing mandatory parameter" in (str(output)):
                shell.send("sh inven 1\n")
                time.sleep(2)
                if shell.recv_ready():
                    output = shell.recv(1000)
        info.append(str(output))
        ssh.close()
    return info

def getData(sheet):
    data = []
    for i in range(sheet.nrows):
        data.append(sheet.cell_value(i, 0))
    return data

def parseInfo(info):
    for num in range(len(info)):
        if not info[num].startswith("Couldn't"):
            text = info[num].partition("DESCR: \"")[2].partition("\"")[0]
            if text.endswith("Stack"):
                text = info[num].partition("DESCR: \"")[2].partition("DESCR: \"")[2].partition("\"")[0]
            info[num] = text
    return info

def writeData(info):
    with open("Switch Types 3.csv", 'w', newline="") as myfile:
        wr = csv.writer(myfile, delimiter = "\n", quoting=csv.QUOTE_ALL)
        wr.writerow(info)


main()
