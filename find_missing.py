#!/bin/bash
import csv
import ipaddress
import sys

# find all missing ipv4 addresses from geoip database
# usage: python3 find_missing.py output/country.csv

f = open(sys.argv[1])

interval = (0, 2 ** 32 - 1)
intervals = []

reader = csv.reader(f)
header = next(reader)

for line in reader:
    if ":" in line[0]:
        # ignore ipv6
        continue
    start = int.from_bytes(ipaddress.ip_address(line[0]).packed, "big")
    end = int.from_bytes(ipaddress.ip_address(line[1]).packed, "big")
    intervals.append((start, end))

f.close()

intervals.sort(key=lambda x: x[0])

if intervals[0][0] != interval[0]:
    print(ipaddress.ip_address(interval[0]), "-", ipaddress.ip_address(intervals[0][0] - 1))

for i in range(len(intervals) - 1):
    if intervals[i][1] < intervals[i + 1][0] - 1:
        print(ipaddress.ip_address(intervals[i][1] + 1), "-", ipaddress.ip_address(intervals[i + 1][0] - 1))

if intervals[-1][1] != interval[1]:
    print(ipaddress.ip_address(intervals[-1][1] + 1), "-", ipaddress.ip_address(interval[1]))
