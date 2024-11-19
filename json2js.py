from optparse import OptionParser
import  json

def main():
    usage = "usage: %prog [-i 'stations.ini' -d 'directory with files in json format' -o 'directory to save output files]"
    parser = OptionParser(usage)
    parser.add_option("-i", "--file", dest="stations_file", default="stations.ini",
                          help="file with LIST of stations with IP addresses")
    parser.add_option("-d", "--dir", dest="path", default=".",
                          help="PATH for files in json format")
    parser.add_option("-o", "--out", dest="outdir", default=".",
                      help="OUTDIR to save status json file for map")

    (options, args) = parser.parse_args()

        # if options.verbose:
        #  print ("stations file %s" % options.stations_file)
        #  print("config directory %s" % options.path)

    process(options.stations_file, options.path, options.outdir)

def process(file, path, outdir):
    import string
    import re
    import os
    import pydash


    #print(file, path)
    stations_file = open(file, 'r')
    line = stations_file.readline().rstrip()
    new_group_json = {}
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
        group_name = station[0:4]

        group_name = group_name.lower()
        #print(group_name)
        new_group_json[group_name] = {}
        #print(new_group_json)
        line = stations_file.readline().rstrip()
    #print(new_group_json)
    stations_file.close()
    stations_file = open(file, 'r')
    line = stations_file.readline().rstrip()
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

        sta_dir = os.path.join(path, station)

        ip_address_splitted = station_ip.split('.')
        if ip_address_splitted[0] == 'localhost':
            json_filename = "%s_localhost.json" % (station)
        else:
            json_filename = "%s_%s_%s_%s_%s.json" % (station, ip_address_splitted[0], ip_address_splitted[1], ip_address_splitted[2], ip_address_splitted[3])
        #json_filename = "%s_%s_%s_%s_%s.json" % (station, ip_address_splitted[0], ip_address_splitted[1], ip_address_splitted[2], ip_address_splitted[3])
        json_dir = os.path.join(path, json_filename)

        new_json_object = {}
        new_sta_json = {}
        new_site_json = {}

        js_object = {}
        if not os.path.exists(json_dir):
            line = stations_file.readline().rstrip()
            continue
        with open(json_dir, "r") as infile:

            json_object = json.load(infile)
            js_station = json_object['Station']

            #print(group_name)
            lon_string = json_object['Longitude']
            lon_splitted = lon_string.split()
            if lon_splitted[0] == '0' or lon_splitted[0] == 'N/A':
                lon = lon_splitted[0]
                #print(lon)
            else:
                lon = float(lon_splitted[0])
            #lon = lon_splitted[0]

            lat_string = json_object['Latitude']
            lat_splitted = lat_string.split()
            if lat_splitted[0] == '0' or lat_splitted[0]== 'N/A':
                lat = lat_splitted[0]
                #print(lat_splitted)
            else:
                lat = float(lat_splitted[0])
            #lat = lat_splitted[0]

            date_string = json_object['Date']
            date_string_splitted = date_string.split()
            js_date = "%s %s" % (date_string_splitted[0], date_string_splitted[1])

            power_string = json_object['Power']
            power_splitted = power_string.split()
            power = float(power_splitted[0])

            if power > 11:
               stat = "ok"
            elif power > 10 and power < 11:
               stat = "warn"
            elif power < 10:
                stat = "bad"


            new_sta_json['date'] = js_date
            new_sta_json['lon'] = lon
            new_sta_json['lat'] = lat
            new_sta_json['name'] = js_station
            new_sta_json['stat'] = stat
            #print(new_sta_json)
            js_station = js_station.lower()
            new_site_json[js_station] = new_sta_json
            group_name = js_station[0:4]

            #group_name = group_name.lower()
            #print(new_site_json)



            #print(json_object)


            new_group_json[group_name][js_station] = new_sta_json

            #.update(new_sta_json)
        #print(new_group_json)
        json_object = json.dumps(new_site_json, indent=4)
        #with open("js_file.json", "wt") as outfile:
        #    json.dump(new_site_json, outfile, indent=4)
        #print(json_object)

        #for key in new_site_json:
        #    pydash.set_(js_object, key, new_site_json[key])

        #print(js_object)
        #json.dump(js_object, js_file, indent=4)
        line = stations_file.readline().rstrip()
    #print(new_group_json)
    json_object = json.dumps(new_group_json, indent=4)
    #print(json_object)
    output_file_name = "status_for_map.json"
    output_path = os.path.join(outdir, output_file_name)

    with open(output_path, "wt") as outfile:
        json.dump(new_group_json, outfile, indent=4)


    #for key in new_group_json:
    #    pydash.set_(js_object, key, new_group_json[key])
    #print(js_object)

    #new_json_object[group_name] = new_site_json
    #print(new_json_object)
    #with open(json_dir, "w") as outfile:


if __name__ == "__main__":
    main()