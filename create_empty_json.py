#!/usr/bin/env python3

from optparse import OptionParser
import  json
from get_seed_time import get_seed_time_process


def main():
    usage = "usage: %prog [-i 'stations.ini' -o 'directory for files in json format']"
    parser = OptionParser(usage)
    parser.add_option("-i", "--file", dest="stations_file", default="stations.ini",
                      help="file with LIST of stations with IP addresses, default 'stations.ini'")
    parser.add_option("-o", "--output", dest="output", default=".",
                      help="PATH to save files in json format, default '.'")

    (options, args) = parser.parse_args()

    # if options.verbose:
    #  print ("stations file %s" % options.stations_file)
    #  print("config directory %s" % options.path)

    process(options.stations_file, options.output)


def process(file, output):
    import string
    import re
    import os
    #print(file, path)
    stations_file = open(file, 'r')

    line = stations_file.readline().rstrip()
    #print(line)

    while (line != ""):
        #print(line)
        if line.find('#') == 0:
            line = stations_file.readline().rstrip()
            continue
        #print("\n")
        #print(line)
        station_line = line.split()
#        print(station_line)
        station_ip_with_port = station_line[0]
        station_ip_with_port_splitted = station_ip_with_port.split(':')
        station_ip = station_ip_with_port_splitted[0]
        if len(station_ip_with_port_splitted) > 1:
            port = station_ip_with_port_splitted[1]
            #url = "http://%s:%s" % (station_ip, port)
            #print(url)
        else:
            #url = "http://%s" % (station_ip)
            port = "80"
            #print(url)

        station = station_line[1]
        #print(station)

        if station_ip[0] == 'localhost':
            json_filename = "%s_localhost_%s.json" % (station, port)
        else:
            station_ip_splitted = station_ip.split('.')
            #print(station_ip_splitted)
            json_filename = "%s_%s_%s_%s_%s_%s.json" % (station, station_ip_splitted[0], station_ip_splitted[1], station_ip_splitted[2], station_ip_splitted[3], port)

        station_json = {}
        channels_json = {}



        station_json['Registration'] = ""
        station_json["Status"] = ""
        station_json["Latency"] = ""
        station_json['Station'] = ""
        station_json['Serial number'] = ""
        station_json['Firmware'] = ""
        station_json['Sampling rate'] = ""
        station_json['Date'] = ""
        station_json['Power'] = ""
        station_json['CPU temp.'] = ""
        station_json['Uptime'] = ""
        station_json['Free size'] = ""
        station_json['HRT'] = ""
        station_json['Time source'] = ""
        station_json['Timegaps'] = ""
        station_json['PPS stab.'] = ""
        station_json['GPS sleep time'] = ""
        station_json['Coords'] = ""
        station_json['Latitude'] = ""
        station_json['Longitude'] = ""
        station_json['Position'] = ""
        station_json['Nav. status'] = ""
        station_json['Time offset'] = ""
        station_json['Last clock sync at'] = ""
        channels_json['Full name'] = ""
        channels_json['Amplitude'] = ""
        channels_json['DC offset'] = ""
        station_json["Channels"] = channels_json
        station_json['Last RESET'] = ""
        station_json['Last soft reboot'] = ""


#        json_object = json.dumps(station_json, indent=4)
#        if len(json_object) != 0:
#           print(json_object)
        json_dir = os.path.join(output, json_filename)
        if len(station_json) != 0:
            if not os.path.exists(output):
                os.makedirs(output)
            with open(json_dir, "w") as outfile:
               json.dump(station_json, outfile, indent=4)
        line = stations_file.readline().rstrip()


if __name__ == "__main__":
    main()
