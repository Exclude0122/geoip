# GEOIP

Convert geoip databases to v2ray format.

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