import socket
import xlrd

def main():
    loc = ("UnreachableDevices.xlsx")
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    device_IPs = getData(sheet)
    displayFQDN(device_IPs)

def getData(sheet):
    data = []
    for i in range(sheet.nrows):
        data.append(sheet.cell_value(i, 0))
    return data

def displayFQDN(ips):
    for ip in ips:
        print(socket.getfqdn(ip))

main()
