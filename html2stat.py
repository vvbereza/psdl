#!/usr/bin/env python3

from optparse import OptionParser
import  json
from get_seed_time import get_seed_time_process


def main():
    usage = "usage: %prog [-i 'stations.ini' -d 'directory for files in json format']"
    parser = OptionParser(usage)
    parser.add_option("-i", "--file", dest="stations_file", default="stations.ini",
                      help="file with LIST of stations with IP addresses")
    parser.add_option("-d", "--dir", dest="path", default=".",
                      help="PATH for html files")
    parser.add_option("-o", "--output", dest="output", default=".",
                      help="PATH to save files in json format")

    (options, args) = parser.parse_args()

    # if options.verbose:
    #  print ("stations file %s" % options.stations_file)
    #  print("config directory %s" % options.path)

    process(options.stations_file, options.path, options.output)


def process(file, path, output):
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
        #print(json_filename)
        json_dir = os.path.join(output, json_filename)
        prev_navstat_json = {}
        prev_navstat_level = {}
        prev_coords_json = {}
        prev_lon_json = {}
        prev_lat_json = {}
        gps_status_json = {}
        prev_gps_status_json = {}
        json_file_exist  = {}
        index_file_exist  = {}
        status = {}
        seed_time = {}
        seed_timestamp = {}
        seed_time_latency = {}
        offline_dict = {}
        #print(json_dir)

        index_name = "%s_index.html" % station
        index_path = os.path.join(path, index_name)
        #print(index_path)


        if os.path.exists(index_path):
            index_file = open(index_path)
            index_line = index_file.readline().rstrip()
#            print(len(index_line))
            if len(index_line) == 0:
                #line = stations_file.readline().rstrip()
                index_file_exist[station] = False
                offline_dict[station] = False
            else:
                index_file_exist[station] = True
                offline_dict[station] = True
            index_file.close()
        else:
            index_file_exist[station] = False

        json_file_exist[station] = True
        station_json = {}
        channels_json = {}
        if os.path.exists(json_dir):
            #print(json_dir)
            with open(json_dir, "r") as infile:
                try:
                    json_object = json.load(infile)
                except:
                    print("JSONDecodeError %s" % infile)
                if index_file_exist[station] == False:
                    station_json = json_object
                    station_json['Status'] = 'offline'
                    status[station] = "offline"
                    json_object = json.dumps(station_json, indent=4)
                    json_dir = os.path.join(output, json_filename)

                    if len(station_json) != 0:
                       if not os.path.exists(output):
                            os.makedirs(output)
                       with open(json_dir, "w") as outfile:
                            json.dump(station_json, outfile, indent=4)

                    line = stations_file.readline().rstrip()
                    continue
                elif os.path.getsize(index_path) == 0:
                    station_json['Status'] = 'offline'
                    status[station] = "offline"


               # print(prev_gps_status_json)
        else:
            #print("json file does not exist")
            json_file_exist[station] = False
            if index_file_exist[station] == False:
                station_json['Registration'] = ""
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
                station_json["Status"] = "offline"
                station_json["Latency"] = "-1"
                json_object = json.dumps(station_json, indent=4)
                #if len(json_object) != 0:
                #   print(json_object)
                json_dir = os.path.join(output, json_filename)
                #print(len(station_json))

                if len(station_json) != 0:
                    if not os.path.exists(output):
                        os.makedirs(output)
                    with open(json_dir, "w") as outfile:
                        json.dump(station_json, outfile, indent=4)

                line = stations_file.readline().rstrip()
                continue

        #print("index_path = %s" % index_path)
        if os.path.exists(index_path):
            index_file = open(index_path)
            index_line = index_file.readline().rstrip()
            #print("index_line = %s" % index_line)
        else:
            index_line = ""
        #print(len(index_line))

        channels_json = {}
        power_dict = {}
        pps_dict = {}
        if json_object:
            station_json = json_object
        while (index_line != ""):
            #print(index_line)
            #index = index_line.find('title')
            #if index:
            #    index_line = index_file.readline().rstrip()
            power_dict[station] = ""
            stat = ""
            station_json['Registration'] = "On"
            index = index_line.find('Registration is STOPPED!!!')
            if index >= 0:
                station_html = index_line[index + 8:index + 13]
                station_json['Registration'] = "Off"

            index = index_line.find('Station')
            if index >= 0:
                station_html = index_line[index + 8:index + 13]
                station_json['Station'] = station_html
            index = index_line.find('Serial number')
            if index >= 0:
                serial_number_item = index_line[index + 34:index + 40]
                serial_number_splitted = serial_number_item.rsplit('<')
                serial_number = serial_number_splitted[0]
                station_json['Serial number'] = serial_number

            index = index_line.find('Firmware')
            if index >= 0:
                firmware_item = index_line[index + 17:index + 32]
                firmware_splitted = firmware_item.rsplit('<')
                firmware = firmware_splitted[0]
                station_json['Firmware'] = firmware

            index = index_line.find('Sampling rate')
            if index >= 0:
                sample_rate_item = index_line[index + 22:index + 25]
                sample_rate_splitted = sample_rate_item.rsplit('<')
                sample_rate = sample_rate_splitted[0]

                station_json['Sampling rate'] = sample_rate

            index = index_line.find('Date')
            if index >= 0:
                date_item = index_line[index + 13:index + 40]
                date_splitted = date_item.rsplit('<')
                date = date_splitted[0]

                station_json['Date'] = date

            index = index_line.find('Power')
            if index >= 0:
                power_item = index_line[index + 14:index + 20]
                power_splitted = power_item.rsplit('<')
                power = power_splitted[0]

                station_json['Power'] = power
#                print(station_json['Power'])
                power_dict[station] = power
            index = index_line.find('CPU temp.')
            if index >= 0:
                cpu_item = index_line[index + 18:index + 25]
                cpu_splitted = cpu_item.rsplit('<')
                cpu = cpu_splitted[0]

                station_json['CPU temp.'] = cpu
            index = index_line.find('Uptime')
            if index >= 0:
                uptime_item = index_line[index + 15:index + 46]
                uptime_splitted = uptime_item.rsplit('<')
                uptime = uptime_splitted[0]

                station_json['Uptime'] = uptime
            index = index_line.find('Free size')
            if index >= 0:
                freesize_item = index_line[index + 18:index + 31]
                freesize_splitted = freesize_item.rsplit('<')
                freesize = freesize_splitted[0]

                station_json['Free size'] = freesize
            index = index_line.find('HRT')
            if index >= 0:
                hrt_item = index_line[index + 12:index + 31]
                hrt_splitted = hrt_item.rsplit('<')
                hrt = hrt_splitted[0]

                station_json['HRT'] = hrt
            index = index_line.find('Time source')
            if index >= 0:
                time_source_item = index_line[index + 20:index + 25]
                time_source_splitted = time_source_item.rsplit('<')
                time_source = time_source_splitted[0]

                station_json['Time source'] = time_source
            index = index_line.find('Timegaps')
            if index >= 0:
                timegaps_item = index_line[index + 17:index + 25]
                timegaps_splitted = timegaps_item.rsplit('<')
                timegaps = timegaps_splitted[0]

                station_json['Timegaps'] = timegaps
            index = index_line.find('PPS stab.')
            pps_stat = "unknown"
            if index >= 0:
                pps_item = index_line[index + 18:index + 25]
                pps_splitted = pps_item.rsplit('<')
                pps = pps_splitted[0]

                station_json['PPS stab.'] = pps
                pps_dict[station] = pps
                if pps_dict and len(pps_dict[station]) != 0:
                    pps_string = pps_dict[station]
                    pps_splitted = pps_string.split('%')
                    pps = float(pps_splitted[0])
                    #print(pps)
                    if pps == 100:
                        pps_stat = "ok"
                    elif pps == 0 or pps < 100 :
                        pps_stat = "warn"
            index = index_line.find('GPS sleep time')
            if index >= 0:
                gps_sleep_time_item = index_line[index + 23:index + 30]
                gps_sleep_time_splitted = gps_sleep_time_item.rsplit('<')
                gps_sleep_time = gps_sleep_time_splitted[0]

                station_json['GPS sleep time'] = gps_sleep_time
            index = index_line.find('Coords')

            index = index_line.find('Nav. status')
            if index >= 0:

                nav_status_item  = index_line[index + 20:index + 30]
                #print(nav_status_item)
                nav_status_item_splitted = nav_status_item.rsplit('<')
                #print(nav_status_item_splitted)
                nav_status = nav_status_item_splitted[0]
                nav_status_splitted = nav_status.split()
                if len(nav_status_splitted) > 1:
                    nav_status_level_items = nav_status_splitted[1]
                    nav_status_level = nav_status_level_items[1:2]
                else:
#                    nav_status_level_items = 'X'
                    nav_status_level = "Unknown"

                #print(nav_status_level)

                station_json['Nav. status'] = nav_status
                print(station, nav_status)

            index = index_line.find('Time offset')
            if index >= 0:

                time_offset_item = index_line[index + 20:index + 35]
                time_offset_splitted = time_offset_item.rsplit('<')
                time_offset = time_offset_splitted[0]

                station_json['Time offset'] = time_offset
            index = index_line.find('Last clock sync at')
            if index >= 0:
                last_clock_sync_item = index_line[index + 27:index + 40]
                last_clock_sync_splitted = last_clock_sync_item.rsplit('<')
                last_clock_sync = last_clock_sync_splitted[0]

                station_json['Last clock sync at'] = last_clock_sync
            index = index_line.find('</th></tr><tr><td>')

            if index >= 0:
                channels_item = index_line[index + 18:index + 40]
                channels_splitted = channels_item.rsplit('<')
                channels = channels_splitted[0]
                chan_len = len(channels)

                channels_json['Full name'] = channels

                amplitude_item = index_line[index + chan_len + 27:index + chan_len + 35]
                amplitude_splitted = amplitude_item.rsplit('<')

                amplitude = amplitude_splitted[0]

                ampl_len = len(amplitude)
                channels_json['Amplitude'] = amplitude

                dc_offset_item = index_line[index + chan_len + ampl_len + 36:index + chan_len + ampl_len + 45]

                dc_offset_splitted = dc_offset_item.rsplit('<')
                dc_offset = dc_offset_splitted[0]

                channels_json['DC offset'] = dc_offset
                station_json["Channels"] = channels_json

            index = index_line.find('Last RESET source is')
            if index >= 0:
                last_reset_item = index_line[index:index + 40]
                last_reset_splitted = last_reset_item.rsplit('<')
                last_reset = last_reset_splitted[0]

                station_json['Last RESET'] = last_reset

            index = index_line.find('Last soft reboot cause is')
            if index >= 0:
                last_reboot_item = index_line[index:index + 70]
                last_reboot_splitted = last_reboot_item.rsplit('<')
                last_reboot = last_reboot_splitted[0]

                station_json['Last soft reboot'] = last_reboot
            #print(power_dict[station])
            power_stat = "unknown"
            seed_time_stat = "unknown"
            stat = "unknown"
            if power_dict and len(power_dict[station]) != 0:
                power_string = power_dict[station]
                power_splitted = power_string.split()
                power = float(power_splitted[0])
                if power >= 11:
                    power_stat = "ok"
                elif power >= 10 and power < 11:
                    power_stat = "warn"
                elif power < 10:
                    power_stat = "bad"
            #print(power_stat)
            #print(station, seed_time)
            #print(seed_time, seed_timestamp, seed_time_latency)

#            seed_time[station], seed_timestamp[station], seed_time_latency[station] = get_seed_time_process(file, path, station)
            seed_time_latency[station] = get_seed_time_process(file, path, station)
            if seed_time_latency[station] == None:
                seed_time_latency[station] = -1
            #print(station, seed_time_latency[station])
            #print(station, seed_time[station], seed_timestamp[station], seed_time_latency[station])
            if seed_time_latency and len(str(seed_time_latency[station])) != 0:
                latency = seed_time_latency[station]
#                print(latency)
                if latency >= 0 and latency < 60:
                        seed_time_stat = "ok"
                elif (latency >= 60 and latency < 300) or latency < 0:
                    seed_time_stat = "warn"
                elif latency >= 300:
                    seed_time_stat = "bad"
 #               elif latency == -1:
 #                   seed_time_stat = "offline"
            else:
                seed_time_stat = "bad"
#            print(pps_stat, power_stat, seed_time_stat)
            if power_stat == "ok" and seed_time_stat == "ok" and pps_stat == 'ok':
                stat = "ok"
            if power_stat == "warn" or seed_time_stat == "warn" or pps_stat == 'warn':
                stat = "warn"
            if power_stat == "bad" or seed_time_stat == "bad":
                stat = "bad"
            if offline_dict[station] == False:
                stat = "offline"
            station_json['Status'] = stat
            station_json['Latency'] = seed_time_latency[station]
            #print(station_json['Status'])
            index_line = index_file.readline().rstrip()
        #print(station_json)
#        station_json['Status'] = gps_status_json[station]
        #ip_address_splitted = station_ip.split('.')
        #if ip_address_splitted[0] == 'localhost':
        #    json_filename = "%s_localhost_%s.json" % (station, port)
        #else:
        #    json_filename = "%s_%s_%s_%s_%s_%s.json" % (station, ip_address_splitted[0], ip_address_splitted[1], ip_address_splitted[2], ip_address_splitted[3], port)
        #print(json_filename)

        json_object = json.dumps(station_json, indent=4)
#        if len(json_object) != 0:
#           print(json_object)
        json_dir = os.path.join(output, json_filename)
        #print(len(station_json))

        if len(station_json) != 0:
            if not os.path.exists(output):
                os.makedirs(output)
            with open(json_dir, "w") as outfile:
               json.dump(station_json, outfile, indent=4)

        line = stations_file.readline().rstrip()


if __name__ == "__main__":
    main()
