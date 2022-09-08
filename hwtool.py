import psutil
import sys
import socket
import cpuinfo
from prettytable import PrettyTable
from psutil._common import bytes2human

def getTemps():
    temps = psutil.sensors_temperatures()
    x = PrettyTable()
    x.title = "TEMPERATURE SENSORS"
    x.align = "c"
    x.field_names = ["Sensor", "Temperature", "High", "Critical"]

    if not temps:
        return

    for name, entries in temps.items():
        for entry in entries:
            x.add_row(
                [entry.label or name or "N/A", entry.current or "N/A", entry.high or "N/A", entry.critical or "N/A"]
            )
    print(x)

def getDiskSpace():
    x = PrettyTable()
    x.title = "DISK USAGE"
    x.align = "c"
    x.field_names = ["Device", "Total", "Used", "Free", "Usage (%)", "Type", "Mount point"]
    parts = psutil.disk_partitions()
    
    for part in parts:
        usage = psutil.disk_usage(part.mountpoint)
        x.add_row(
            [part.device, bytes2human(usage.total), bytes2human(usage.used), bytes2human(usage.free), str(int(usage.percent)) + "%", part.fstype, part.mountpoint]
        )

    print (x)

def getNetworkInfo():
    addrs = psutil.net_if_addrs()
    x = PrettyTable()
    x.title = "NETWORK INFORMATION"
    x.align = "c"
    x.field_names = ["Device", "IPv4 Address", "Netmask"]
    
    for nic, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                x.add_row( [nic, addr.address, addr.netmask or "N/A"] )
    print(x)    

def getCPUInfo():
    arch = cpuinfo.get_cpu_info()['arch']
    cpu = cpuinfo.get_cpu_info()['brand_raw']
    clock_current = cpuinfo.get_cpu_info()['hz_actual_friendly']
    clock_advertised = cpuinfo.get_cpu_info()['hz_advertised_friendly']
    x = PrettyTable()
    x.title = "CPU INFORMATION"
    x.align = "c"
    x.field_names = ["Architecture", "Model", "Current frequency", "Advertised frequency"]
    x.add_row( [arch, cpu, clock_current, clock_advertised] )
    print(x)

def main():
    getTemps()
    getDiskSpace()
    getNetworkInfo()
    getCPUInfo()

if __name__ == "__main__":
    sys.exit(main())