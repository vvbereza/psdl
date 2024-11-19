#!/usr/bin/env python3

from optparse import OptionParser
import  json

def main():
    usage = "usage: %prog [-i 'stations.ini' -d 'directory with files in json format' -t 'PSDL template ini file' -p 'PSDL ini file']"
    parser = OptionParser(usage)
    parser.add_option("-i", "--file", dest="stations_file", default="stations.ini",
                          help="file with LIST of stations with IP addresses")
    parser.add_option("-d", "--dir", dest="path", default=".",
                          help="PATH for files in json format")
    parser.add_option("-t", "--template", dest="template", default="psdl.ini",
                          help="PSDL template ini file with full or relative path")
    parser.add_option("-p", "--psdl", dest="psdl", default="psdl.ini",
                          help="PSDL ini file with full or relative path. It can be the same as template psdl.ini")

    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")

    (options, args) = parser.parse_args()

    process(options.stations_file, options.path, options.template, options.psdl, options.verbose)

def process(file, path, template, psdl, verbose):
    import os


    #print(file, path, template, psdl, verbose)
    stations_file = open(file, 'r')
    line = stations_file.readline().rstrip()

    lat_json = {}
    lon_json = {}

    while (line != ""):
        # print(line)
        if line.find('#') == 0:
            line = stations_file.readline().rstrip()
            continue
        station_line = line.split()
        station_ip_with_port = station_line[0]
        station_ip_with_port_splitted = station_ip_with_port.split(':')
        station_ip = station_ip_with_port_splitted[0]
        station = station_line[1]
        if len(station_ip_with_port_splitted) > 1:
            station_port = station_ip_with_port_splitted[1]

        ip_address_splitted = station_ip.split('.')
        if ip_address_splitted[0] == 'localhost':
            if station_port:
                json_filename = "%s_localhost_%s.json" % (station, station_port)
            else:
                json_filename = "%s_localhost.json" % (station)
        else:
            if station_port:
                json_filename = "%s_%s_%s_%s_%s_%s.json" % (station, ip_address_splitted[0], ip_address_splitted[1], ip_address_splitted[2], ip_address_splitted[3], station_port)
            else:
                json_filename = "%s_%s_%s_%s_%s.json" % (station, ip_address_splitted[0], ip_address_splitted[1], ip_address_splitted[2], ip_address_splitted[3])
        #json_filename = "%s_%s_%s_%s_%s.json" % (station, ip_address_splitted[0], ip_address_splitted[1], ip_address_splitted[2], ip_address_splitted[3])
        json_dir = os.path.join(path, json_filename)
        #print(json_dir)

        if not os.path.exists(json_dir):
            line = stations_file.readline().rstrip()
            continue
        with open(json_dir, "r") as infile:
            json_object = json.load(infile)
            #print(json_object)
            if 'Longitude' in json_object:
                lon_string = json_object['Longitude']
                lon_splitted = lon_string.split()
                #print(lon_splitted)
            else:
                lon_string = ""
                print("%s: no Longitude in %s" % (station, json_dir))

            #print(lon_splitted)
            if len(lon_splitted) > 0 and (lon_splitted[0] == '0' or lon_splitted[0] == 'N/A'):
                lon = lon_splitted[0]
                #print(lon)
            else:
                lon = float(lon_splitted[0])
                if len(lon_splitted) > 0:
                    lat = float(lon_splitted[0])
                else:
                    lon = '0'
                #print(lon)
            lon_json[station] = lon

            if 'Latitude' in json_object:
                lat_string = json_object['Latitude']
                lat_splitted = lat_string.split()
                #print(lat_splitted)
            else:
                lat_string = ""
                print("%s: no Latitude in %s" % (station, json_dir))

            #print(lat_splitted[0])
            if len(lat_splitted) > 0 and (lat_splitted[0] == '0' or lat_splitted[0]== 'N/A'):
                lat = lat_splitted[0]
                #print(lat_splitted)
            else:
                if len(lat_splitted) > 0:
                    lat = float(lat_splitted[0])
                else:
                    lat = '0'
                #print(lat)
            lat_json[station] = lat

        line = stations_file.readline().rstrip()

    psdl_in = open(template, "rt")
    psdl_lines = psdl_in.readlines()

    psdl_in.close()

    psdl_out = open(psdl, "wt")

    if verbose:
        print("Template PSDL config file %s" % template)
        print("PSDL config file %s" % psdl)

    sum_of_lats = 0.0
    n = len(lat_json)
    for key in lat_json:
        if lat_json[key] == '0' or lat_json[key] == 'N/A':
            continue
        else:
            sum_of_lats = sum_of_lats + lat_json[key]

    if n == 0:
        n = 1
    center_lat = round(sum_of_lats/n, 6)
    #print(center_lat, n)

    sum_of_lons = 0.0
    n = len(lon_json)
    if n == 0:
        n = 1
    for key in lon_json:
        if lon_json[key] == '0' or lon_json[key] == 'N/A':
            continue
        else:
            sum_of_lons = sum_of_lons + lon_json[key]

    center_lon = round(sum_of_lons/n, 6)
    #print(center_lon, n)

    for psdl_line in psdl_lines:
        #psdl_line = psdl_line.rstrip()
        #print(psdl_line)
        string_to_look_for = "Sensor"
        index = psdl_line.find(string_to_look_for)
        if index >= 0:
            #print(psdl_line)
            sensor_line_splitted = psdl_line.rsplit('=')
            #print(sensor_line_splitted)
            staname_splitted = sensor_line_splitted[2].rsplit()
            staname = staname_splitted[0][1:5]
            #print(staname)
            sensname_splitted = sensor_line_splitted[3].rsplit()
            #print(sensname_splitted[0])
            sensname = sensname_splitted[0]
            sensnumber = sensname[3:4]
            #print(sensnumber)
            sitename = "%s%s" % (staname, sensnumber)
            #print(sitename)
            staname_to_find_string = staname
            staname_index = psdl_line.find(staname_to_find_string)
            if staname_index >0:
                for key in lat_json:
                    #print(key, lat_json[key])
                    if key == sitename:
                        #print(psdl_line)
                        psdl_line = "  Sensor=(StatName='%s' SensName='BD%s' Fi=%s  Ld=%s   Multiplier=1)\n" % (staname, sensnumber, lat_json[key], lon_json[key])
                        #print(psdl_line)
        """
        index = psdl_line.find("Fi0")
        if index >= 0:
            #print(psdl_line)
            psdl_line = "  Fi0=%f {Координаты центра}\n" % center_lat
            #print(psdl_line)

        index = psdl_line.find("Ld0")
        if index >= 0:
            #print(psdl_line)
            psdl_line = "  Ld0=%f\n" % center_lon
            #print(psdl_line) 
        """

        psdl_out.write(psdl_line)

    psdl_out.close()

if __name__ == "__main__":
    main()
