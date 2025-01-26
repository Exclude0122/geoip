import argparse
import csv
import sys
import ipaddress
import geoip_pb2
import os

parser = argparse.ArgumentParser(
    prog="geoip",
)
parser.add_argument("input", help="input csv file")
parser.add_argument("-o", "--output", help="output file", default="geoip.dat")
parser.add_argument("--text", help="text output")
parser.add_argument(
    "-f", "--filter", help="country code filter", action="append", default=[]
)

args = parser.parse_args()

# country code => list of CIDRs
ipv4 = {}
ipv6 = {}

# read csv file
print("Reading input csv...")
with open(args.input) as f:
    reader = csv.reader(f)

    header = next(reader)
    if "start_ip" not in header or "end_ip" not in header or "country" not in header:
        raise ValueError("input csv header must contain start_ip, end_ip and country")

    start_ip_idx = header.index("start_ip")
    end_ip_idx = header.index("end_ip")
    country_idx = header.index("country")

    for line in reader:
        start_ip = ipaddress.ip_address(line[start_ip_idx])
        end_ip = ipaddress.ip_address(line[end_ip_idx])
        country = line[country_idx].lower()

        if len(args.filter) > 0 and country not in args.filter:
            continue

        if country not in ipv4:
            ipv4[country] = []
        if country not in ipv6:
            ipv6[country] = []

        cidrs = list(ipaddress.summarize_address_range(start_ip, end_ip))
        if isinstance(cidrs[0], ipaddress.IPv4Network):
            ipv4[country].extend(cidrs)
        else:
            ipv6[country].extend(cidrs)

# special ips
if len(args.filter) == 0 or "private" in args.filter:
    ipv4["private"] = [
        ipaddress.ip_network(i)
        for i in [
            "0.0.0.0/8",
            "10.0.0.0/8",
            "100.64.0.0/10",
            "127.0.0.0/8",
            "169.254.0.0/16",
            "172.16.0.0/12",
            "192.0.0.0/24",
            "192.0.2.0/24",
            "192.88.99.0/24",
            "192.168.0.0/16",
            "198.18.0.0/15",
            "198.51.100.0/24",
            "203.0.113.0/24",
            "224.0.0.0/4",
            "240.0.0.0/4",
            "255.255.255.255/32",
        ]
    ]
    ipv6["private"] = [
        ipaddress.ip_network(i)
        for i in [
            "::/128",
            "::1/128",
            "fc00::/7",
            "fe80::/10",
            "ff00::/8",
        ]
    ]
ipv4["test"] = [ipaddress.ip_network("127.0.0.0/8")]

# sort & merge
print("Sorting...")
for k in ipv4:
    ipv4[k].sort()
    ipv4[k] = list(ipaddress.collapse_addresses(ipv4[k]))

for k in ipv6:
    ipv6[k].sort()
    ipv6[k] = list(ipaddress.collapse_addresses(ipv6[k]))

# output
print("Writing output...")
countries = sorted(set(ipv4.keys()).union(ipv6.keys()))

geoipList = geoip_pb2.GeoIPList()
for c in countries:
    geoip = geoipList.entry.add()
    geoip.country_code = c.upper()

    if c in ipv4:
        for i in ipv4[c]:
            cidr = geoip.cidr.add()
            cidr.ip = i.network_address.packed
            cidr.prefix = i.prefixlen
    if c in ipv6:
        for i in ipv6[c]:
            cidr = geoip.cidr.add()
            cidr.ip = i.network_address.packed
            cidr.prefix = i.prefixlen

with open(args.output, "wb") as f:
    f.write(geoipList.SerializeToString())

# text output
if args.text is not None:
    os.makedirs(args.text, exist_ok=True)

    print("Writing text output...")
    for c in countries:
        f = open(os.path.join(args.text, c.lower() + ".txt"), "w")

        if c in ipv4:
            for i in ipv4[c]:
                f.write(i.compressed + "\n")
        if c in ipv6:
            for i in ipv6[c]:
                f.write(i.compressed + "\n")

        f.close()
