import psutil
import sys
from prettytable import PrettyTable
from psutil._common import bytes2human

def getTemps():
    temps = psutil.sensors_temperatures()

    if not temps:
        sys.exit("No temperature sensors available. Exiting...")

    for name, entries in temps.items():
        x = PrettyTable()
        x.field_names = ["Sensor", "Temperature", "High", "Critical"]
        for entry in entries:
            x.add_row(
                [entry.label or name or "N/A", entry.current or "N/A", entry.high or "N/A", entry.critical or "N/A"]
            )
        print(x)

def getDiskSpace():

    x = PrettyTable()
    x.field_names = ["Device", "Total", "Used", "Free", "Use", "Type", "Mount"]
    parts = psutil.disk_partitions(all=False)
    for part in parts:
        usage = psutil.disk_usage(part.mountpoint)
        x.add_row(
            [part.device, bytes2human(usage.total), bytes2human(usage.used), bytes2human(usage.free), int(usage.percent), part.fstype, part.mountpoint]
        )
    print (x)

def main():
    getTemps()
    getDiskSpace()

if __name__ == "__main__":
    sys.exit(main())