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
    count = 1
    with open(os.devnull, "wb") as limbo:
        for ip in ips:
            result = subprocess.Popen(["ping", "-n", "1", "-w", "200", ip], stdout=limbo, stderr=limbo).wait()
            if result:
                print(ip, "\t: failed")
                info[ip] = "NO"
                nos += 1
            else:
                print(ip, "\t: passed")
                info[ip] = "YES"
                yes += 1
    print("Failed: ", nos, "\nPassed: ", yes, " (", count, "/", length, ")")
    return info

main()
