$ python D:\work\POLYGON2023\scripts\html2json.py -i D:\work\POLYGON2023\config\stations.ini -d D:\work\POLYGON2023\status

$ python D:\work\POLYGON2023\scripts\html2json.py -h

Usage: html2json.py [-i 'stations.ini' -d 'directory for files in json format]'

Options:
  -h, --help            show this help message and exit
  -i STATIONS_FILE, --file=STATIONS_FILE
                        file with LIST of stations with IP addresses
  -d PATH, --dir=PATH   PATH to save files in json format

$ python D:\work\POLYGON2023\scripts\json2psdl.py  -d D:\work\POLYGON2023\status -t D:\work\PSDL_ini_v4 -j D:\work\polygon2023

Usage: json2psdl.py [-i 'stations.ini' -d 'directory with files in json format -t 'PSDL template directory']'
Options:
  -h, --help            show this help message and exit
  -i STATIONS_FILE, --file=STATIONS_FILE
                        file with LIST of stations with IP addresses
  -d PATH, --dir=PATH   PATH for files in json format
  -t TEMPLATES, --template=TEMPLATES
                        PSDL template directory
  -j JDIR, --json=JDIR  Root DIR for BACL, PSDL and BM ini files
  -v, --verbose

$ python D:\work\POLYGON2023\scripts\json2psdl.py  -h

Usage: json2psdl.py [-i 'stations.ini' -d 'directory with files in json format -t 'PSDL template directory' -j 'Root directory for PSDL ini files']]'

Options:
  -h, --help            show this help message and exit
  -i STATIONS_FILE, --file=STATIONS_FILE
                        file with LIST of stations with IP addresses, default is station.ini
  -d PATH, --dir=PATH   PATH for files in json format, default is '.'
  -t TEMPLATES, --template=TEMPLATES
                        PSDL template directory
  -j JDIR, --json=JDIR  Root DIR for BACL, PSDL and BM ini files, default is '.'
  -v, --verbose

$ python D:\work\POLYGON2023\scripts\json2js.py -i D:\work\POLYGON2023\config\stations.ini -d D:\work\POLYGON2023\status -o D:\work\POLYGON2023\www

$ python D:\work\POLYGON2023\scripts\json2js.py -h

Usage: json2js.py [-i 'stations.ini' -d 'directory with files in json format' -o 'directory to save output files]

Options:
  -h, --help            show this help message and exit
  -i STATIONS_FILE, --file=STATIONS_FILE
                        file with LIST of stations with IP addresses
  -d PATH, --dir=PATH   PATH for files in json format
  -o OUTDIR, --out=OUTDIR
                        OUTDIR to save status json file for map
