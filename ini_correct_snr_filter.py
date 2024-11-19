#!/usr/bin/env python3
#StationCount = 2
import re

from optparse import OptionParser

def main():
    usage = "usage: %prog -i 'PSDL ini file'-r 'PSDL runtime ini file' "
    parser = OptionParser(usage)
    parser.add_option("-i", "--ini", dest="ini", default="psdl.ini",
                          help="PSDL init file with full or relative path, default is psdl.ini")
    parser.add_option("-r", "--runini", dest="runini", default="psdl_runtime.ini",
                      help="PSDL runtime ini file, default is psdl_runtime.ini")

    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("--debug",
                      action="store_true", dest="debug")

    (options, args) = parser.parse_args()

    process(options.ini, options.runini, options.verbose, options.debug)

def process(ini, runini, verbose, debug):

    sense = input(
        "1 – высокая чувствительность\r\n\
2 – средняя чувствительность\r\n\
3 – низкая чувствительность\r\n\
Выберите чувствительность системы (1,2 или 3):")

    if sense == '1':
        str_snr_out = '\tSNR=3\r'
    elif sense == '2':
        str_snr_out = '\tSNR=5\r'
    else:
        str_snr_out = '\tSNR=7\r'



    filter = input("\r\n\r\n\
1 – локация выстрелов\r\n\
2 – локация выстрелов, разрывов, сбросов\r\n\
Выберите чувствительность системы (1 или 2):")

    if filter == '1':
        str_filter_out = '\tFilter=(Freq0=2  Freq1=8  HalfWind=0.5)\r'
    else:
        str_filter_out = '\tFilter=(Freq0=1  Freq1=25  HalfWind=0.5)\r'



            
    with open(ini) as f:
        lines = f.readlines()
        str_snr = 'SNR='
        str_filter = 'Filter=(Freq0'
        pattern_snr = re.compile(re.escape(str_snr))
        pattern_filter = re.compile(re.escape(str_filter))
    f.close()

    with open(ini, 'w') as f:
        for line in lines:
            result = pattern_snr.search(line)
            result_filter = pattern_filter.search(line)
        
            if (not result) and (not result_filter):
                f.write(line)
            elif result:
                f.write(str_snr_out)
            elif result_filter:
                f.write(str_filter_out)

    f.close()

    with open(runini) as f:
        lines = f.readlines()
        str_snr = 'SNR='
        str_filter = 'Filter=(Freq0'
        pattern_snr = re.compile(re.escape(str_snr))
        pattern_filter = re.compile(re.escape(str_filter))
    f.close()

    with open(runini, 'w') as f:
        for line in lines:
            result = pattern_snr.search(line)
            result_filter = pattern_filter.search(line)

            if (not result) and (not result_filter):
                f.write(line)
            elif result:
                f.write(str_snr_out)
            elif result_filter:
                f.write(str_filter_out)

    f.close()

if __name__ == "__main__":
    main()
