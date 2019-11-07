#!/usr/bin/env python3

import pprint
import sys
from dataclasses import dataclass
from datetime import datetime

import matplotlib.pyplot as plt


@dataclass
class FileData:
    size_bytes: int
    birth_ts: int

def group_by(arr, f):
    grouped = {}
    for el in arr:
        key = f(el)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(el)
    return grouped

def pretty_date(ts):
    return datetime.utcfromtimestamp(ts)#<<<.strftime('%Y-%m-%d %H:%M:%S')

def pretty_bytes(size_bytes):
    return size_bytes / 1024 / 1024 / 1024

def visualize(ts_and_disk_usage):
    x = [pretty_date(ts) for ts, _ in ts_and_disk_usage]
    y = [pretty_bytes(disk_usage) for _, disk_usage in ts_and_disk_usage]
    plt.plot(x, y)
    plt.show()
    pprint.pprint([(pretty_date(ts), pretty_bytes(disk_usage)) for ts, disk_usage in ts_and_disk_usage])

def main():
    file_datas = []
    for data in sys.stdin.readlines():
        birth_ts, size_bytes = data.split()
        file_datas.append(FileData(
            size_bytes=int(size_bytes),
            birth_ts=int(birth_ts),
        ))

    file_data_by_birth_ts = group_by(file_datas, lambda file_data: file_data.birth_ts)
    timestamps = sorted(list(file_data_by_birth_ts.keys()))

    # [
    #    (monday, 1GB),
    #    (tuesday, 2GB),
    # ]
    ts_and_disk_usage = []
    for timestamp in timestamps:
        new_space_used = sum(fd.size_bytes for fd in file_data_by_birth_ts[timestamp])
        if len(ts_and_disk_usage) > 0:
            _, prev_disk_usage = ts_and_disk_usage[-1]
        else:
            prev_disk_usage = 0
        new_disk_usage = prev_disk_usage + new_space_used
        ts_and_disk_usage.append((timestamp, new_disk_usage))

    visualize(ts_and_disk_usage)


if __name__ == "__main__":
    main()
