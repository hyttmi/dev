import psutil
import sys
import socket
from prettytable import PrettyTable
from psutil._common import bytes2human

def getTemps():
    temps = psutil.sensors_temperatures()

    if not temps:
        sys.exit("No temperature sensors available. Exiting...")

    for name, entries in temps.items():
        x = PrettyTable()
        x.title = "TEMPERATURE SENSORS"
        x.field_names = ["Sensor", "Temperature", "High", "Critical"]
        for entry in entries:
            x.add_row(
                [entry.label or name or "N/A", entry.current or "N/A", entry.high or "N/A", entry.critical or "N/A"]
            )
        print(x)

def getDiskSpace():
    x = PrettyTable()
    x.title = "DISK USAGE"
    x.field_names = ["Device", "Total", "Used", "Free", "Use", "Type", "Mount"]
    parts = psutil.disk_partitions(all=False)
    for part in parts:
        usage = psutil.disk_usage(part.mountpoint)
        x.add_row(
            [part.device, bytes2human(usage.total), bytes2human(usage.used), bytes2human(usage.free), int(usage.percent), part.fstype, part.mountpoint]
        )
    print (x)

def getNetworkInfo():
    addrs = psutil.net_if_addrs()
    x = PrettyTable()
    x.title = "NETWORK INFORMATION"
    x.field_names = ["Device", "IPv4 Address", "Netmask"]
    for nic, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                x.add_row( [nic, addr.address, addr.netmask or "N/A"] )
    print(x)    

def main():
    getTemps()
    getDiskSpace()
    getNetworkInfo()

if __name__ == "__main__":
    sys.exit(main())