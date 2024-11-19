from optparse import OptionParser
import  json
import subprocess

def main():
    usage = "usage: %prog [-i 'stations.ini' -d 'directory with files in json format' -o 'directory to save output files -s 'status file name']"
    parser = OptionParser(usage)

    parser.add_option("-i", "--file", dest="stations_file", default="stations.ini",
                          help="file with LIST of stations with IP addresses")
    parser.add_option("-d", "--dir", dest="path", default=".",
                          help="PATH for files in json format")
    (options, args) = parser.parse_args()

        # if options.verbose:
        #  print ("stations file %s" % options.stations_file)
        #  print("config directory %s" % options.path)

    process(options.stations_file, options.path)

def process(file, path):
    import string
    import re
    import os
    import pydash

    #print(file, path, output_path)
    stations_file = open(file, 'r')
    line = stations_file.readline().rstrip()
    new_group_json = {}
    new_group_list = []
    js_pos = ""
    station_addr = {}
    status = {}
    offline = {}
    registration_status = {}
    while (line != ""):
        # print(line)
        if line.find('#') == 0:
            line = stations_file.readline().rstrip()
            continue
        station_line = line.split()
        station_ip_with_port = station_line[0]

        station_ip_with_port_splitted = station_ip_with_port.split(':')
        station_ip = station_ip_with_port_splitted[0]

        if len(station_ip_with_port_splitted) > 1:
            port = station_ip_with_port_splitted[1]
            url = "http://%s:%s" % (station_ip, port)
            #print(url)
        else:
            url = "http://%s" % (station_ip)
            port = "80"
            #print(url)
        station = station_line[1]


        station_addr[station] = url

        #print(group_name)

        #print(new_group_json)
        line = stations_file.readline().rstrip()
    #print(new_group_json)
    stations_file.close()
    stations_file = open(file, 'r')
    line = stations_file.readline().rstrip()
    #print(line)

    while (line != ""):
        #print(line)
        if line.find('#') == 0:
            line = stations_file.readline().rstrip()
            continue
        #print(line)
        station_line = line.split()
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
            #print(url)

        station = station_line[1]
        station_base_index = station.find("A1")
        if station_base_index >= 0:
            station_base_name = station

        sta_dir = os.path.join(path, station)

        ip_address_splitted = station_ip.split('.')
        if ip_address_splitted[0] == 'localhost':
            json_filename = "%s_localhost_%s.json" % (station, port)
        else:
            json_filename = "%s_%s_%s_%s_%s_%s.json" % (station, ip_address_splitted[0], ip_address_splitted[1], ip_address_splitted[2], ip_address_splitted[3], port)
        #json_filename = "%s_%s_%s_%s_%s.json" % (station, ip_address_splitted[0], ip_address_splitted[1], ip_address_splitted[2], ip_address_splitted[3])
        json_dir = os.path.join(path, json_filename)
        #print(json_dir)

        new_json_object = {}
        new_sta_json = {}
        new_site_json = {}
       #status = {}
        js_object = {}
        if not os.path.exists(json_dir):
            line = stations_file.readline().rstrip()
            continue
        with open(json_dir, "r") as infile:
            json_object = json.load(infile)
            #js_station = json_object['Station']
            if 'Nav. status' in json_object:
                js_nav_stat = json_object['Nav. status']
            else:
                js_nav_stat = ""

            offline[station] = json_object['Status']
#            print(online[station])
            registration_status[station] = json_object['Registration']
           # print(group_name)


            status[station] = js_nav_stat



        line = stations_file.readline().rstrip()
        #print(line)

    start_reg_A1 = True
    there_is_A1 = False
    registration_name = ""
    registration_addr = ""
    registration_status_A1 = ""
    reg_status = 0
    noffline = 0
    n_nostatus = 0
    #print(status)
    for key in offline:
        if offline[key] == "offline":
            noffline += 1
    #print(noffline)
    for key in status:
        if not status[key]:
            n_nostatus += 1
    #print(n_nostatus)
    for key in status:
        #print(key, status[key])
#        print(n_nostatus, noffline, reg_status)
        if n_nostatus == 4 or noffline == 4:
            there_is_A1 = False
            start_reg_A1 = False
#            print("n_nostatus == 4 or noffline == 4")
#            print(reg_status)
            registration_name = station_base_name
            break
        index = key.find("A1")
        if index >= 0:
            #print(index)
            there_is_A1 = True
        if index < 0 and there_is_A1:
            #print(key)
            nav_status_items = status[key].split()
            nav_status = status[key]
            #print(key, nav_status, nav_status_items)
            if nav_status_items and len(nav_status_items) > 1:
                nav_status_level = nav_status_items[1][1:2]
            else:
                break
            #print(nav_status_level)
            #if nav_status != 'R (1)' or registration_status[key] == 'On':
            if nav_status_level != '1' or registration_status_A1 == 'On':
                start_reg_A1 = False
                #if registration_status[key] == 'On':
                #    print("registration of %s already 'On'" % registration_name)
                reg_status = 1
                break
            else:
                #print(nav_status_level)
                reg_status += 1
        elif index >= 0 and there_is_A1:
#            print("%s is not reachable yet" % key)
            there_is_A1 = True
            if not os.path.exists('log'):
                os.makedirs('log')
            log_name = "%s_index.html" % station
            logpath = os.path.join('log', log_name)

            wget_command = "wget %s/registration_start -O %s" % (station_addr[key], logpath)
            registration_name = key
            registration_addr = station_addr[key]
            registration_status_A1 = registration_status[key]
            #print(wget_command)
            #print(registration_status_A1)
            #break
        elif index >= 0 and there_is_A1 and registration_status[key] == 'On':
            start_reg_A1 = False
            registration_status_A1 = 'On'

        #print(status[key], station_addr[key])
    #print(reg_status)
    if start_reg_A1:

        if reg_status == 3:
            try:
                print("start registration A1")
                subprocess.check_output(wget_command, stderr=subprocess.PIPE, shell=True)
            except:
                print("can't start registration to %s %s" % (registration_addr, registration_name))
        else:
            print("not all registrators are online yet. So, no registration start for %s yet" % registration_name)
    elif registration_status_A1 == 'On':
        print("the registration is already 'On'. So, no registration start for %s needed" % registration_name)
    elif reg_status == 0:
        if noffline > 0 and noffline <= 4:
            print("not all registrators are online yet. So, no registration start for %s yet" % registration_name)
        elif noffline == 4:
            print("none of the registrators are online yet. So, no registration start for %s yet" % registration_name)
    else:
        print("not all registrators are fixed yet. So, no registration start for %s yet" % registration_name)


if __name__ == "__main__":
    main()
