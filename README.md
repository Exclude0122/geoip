# GEOIP

Convert geoip databases to v2ray format.

## Releases

- [geoip.dat](https://github.com/Exclude0122/geoip/releases/latest/download/geoip.dat)
- [geoip-only-cn-private.dat](https://github.com/Exclude0122/geoip/releases/latest/download/geoip-only-cn-private.dat)
- [geoip-only-ir-private.dat](https://github.com/Exclude0122/geoip/releases/latest/download/geoip-only-ir-private.dat)
- [geoip-only-kp-private.dat](https://github.com/Exclude0122/geoip/releases/latest/download/geoip-only-kp-private.dat)
- [geoip-only-ru-private.dat](https://github.com/Exclude0122/geoip/releases/latest/download/geoip-only-ru-private.dat)
- [private.dat](https://github.com/Exclude0122/geoip/releases/latest/download/private.dat)

IP address data powered by [IPinfo](https://ipinfo.io)

## Usage

```
usage: geoip [-h] [-o OUTPUT] [--text TEXT] [-f FILTER] input

positional arguments:
  input                input csv file

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  output file
  --text TEXT          text output
  -f, --filter FILTER  country code filter
```

Convert csv to geoip.dat

```
python3 main.py country.csv
```

Convert csv to geoip.dat and only inlcude `cn` and `private`

```
python3 main.py country.csv --filter cn --filter private
```

Convert csv to text format and write to `text1` folder:

```
python3 main.py contry.csv --text text1
```

## Data sources

https://db-ip.com/db/download/ip-to-country-lite

https://ipinfo.io/products/free-ip-database