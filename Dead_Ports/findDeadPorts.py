import paramiko
import sys
import time
import xlrd
import xlsxwriter

def main():
    loc = ("switches.xlsx")
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    switches = getSwitches(sheet)
    info = getInfo(switches)
    writeData(info)
    writeDateText(info)

def getSwitches(sheet):
    data = []
    for i in range(sheet.nrows):
        data.append(sheet.cell_value(i, 0))
    return data

def getInfo(switches_list):
    nbytes = 4096
    username = "***Enter username here***"
    password = "***Enter password here***"
    info = []
    output = ""
    switches = {}
    for switch in switches_list:
        print("Working on " + switch)
        port = 22
        switches[switch] = {}
        hostname = switch
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname, port = port, username = username, password = password)
        except paramiko.ssh_exception.AuthenticationException:
            print("Could not authenticate to host " + hostname)
            continue
        except paramiko.ssh_exception.NoValidConnectionsError:
            print("Could not connect to host " + hostname)
            continue
        except:
            print("Unknown Error with host " + hostname)
            continue
        time.sleep(2)
        print ("Successfully connected to " + hostname)
        shell = ssh.invoke_shell()
        time.sleep(2)
        output = shell.recv(2000)
        print("Running commands...")
        shell.send("terminal length 0\n")
        time.sleep(1)
        print("Getting port info...")
        shell.send("sh int status\n")
        time.sleep(2)
        if shell.recv_ready():
            output = shell.recv(16000)
        info = output.decode("ascii")
        ports = getPorts(info)
        for port in ports:
            print("Reading port", port)
            command = "sh int " + port + " | i Last input"
            shell.send(command + "\n")
            time.sleep(.2)0\
            if shell.recv_ready():
                output = shell.recv(2000)
                status = output.decode("ascii")
            status = status.split("\n")
            print(status)
            ports[port] = status[1].strip()
        switches[switch] = ports
        shell.send("terminal length 48\n")
        time.sleep(1)
        shell.close()
        ssh.close()
        print("Finished with switch " + hostname)
    return switches

def getPorts(info):
    ports = {}
    info = info.split("\n")[4:-1]
    for item in info:
        temp = item.split(" ")
        ports[temp[0]] = ""
    return ports

def writeData(switches):
    wb = xlsxwriter.Workbook("Port Usage Info.xlsx")
    ws = wb.add_worksheet()
    row = 0
    col = 0
    ws.set_column('C:C', 50)
    for switch in switches:
        ws.write(row, col, switch)
        row += 1
        col = 1
        for port in switches[switch]:
            ws.write(row, col, port)
            col = 2
            ws.write(row, col, switches[switch][port])
            col = 1
            row += 1
        col = 0
    wb.close()

def writeDateText(switches):
    for switch in switches:
        file = open(switch + " Port Usage Info.txt", "w")
        for port in switches[switch]:
            file.write(port + " : " + switches[switch][port] + "\n")
        file.close()

main()
