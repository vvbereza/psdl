#!/usr/bin/env python3

from optparse import OptionParser
import subprocess
from wget_seed_time_lib import wget_seed_time_process


def main():
    usage = "usage: %prog [-i 'stations.ini' -d 'directory for index.html' -t 'number of tries to connect' -T 'timeout for wget']"
    parser = OptionParser(usage)
    parser.add_option("-i", "--file", dest="stations_file", default="stations.ini",
                      help="file with LIST of stations with IP addresses")
    parser.add_option("-d", "--dir", dest="path", default=".",
                      help="PATH to save index.html files")
    parser.add_option("-t", "--try", dest="n_try", default="3",
                      help="number of tries for wget to connect")
    parser.add_option("-T", "--timeout", dest="timeout", default="12",
                      help="timeout for wget conection")

    (options, args) = parser.parse_args()

    # if options.verbose:
    #  print ("stations file %s" % options.stations_file)
    #  print("config directory %s" % options.path)

    process(options.stations_file, options.path, options.n_try, options.timeout)


def process(file, path, n_try, timeout):
    import string
    import re
    import os
    import shutil

    stations_file = open(file, 'r')

    line = stations_file.readline().rstrip()
    #print(len(line))

    while (line != ""):
        #print(line)
        if line.find('#') == 0:
            line = stations_file.readline().rstrip()
            continue
        #print("\n")
        #print(line)
        station_line = line.split()
        #print(station_line)
        station_ip_with_port = station_line[0]
        station_ip_with_port_splitted = station_ip_with_port.split(':')
        station_ip = station_ip_with_port_splitted[0]
        if len(station_ip_with_port_splitted) > 1:
            port = station_ip_with_port_splitted[1]
            url = "http://%s:%s" % (station_ip, port)
            #print(url)
        else:
            url = "http://%s" % (station_ip)
            #print(url)

        station = station_line[1]
        #print(station)

        #sta_dir = os.path.join(path, station)

        if not os.path.exists(path):
            os.makedirs(path)
        index_name_temp = "%s_index_temp.html" % station
        index_name = "%s_index.html" % station
        savename_temp = os.path.join(path, index_name_temp)
        savename = os.path.join(path, index_name)
        #print(savename_temp)
        #print(savename)
        got_status = False
        try:
            wget_command = "wget %s -t %s -T %s -O %s" % (url, n_try, timeout, savename_temp)
            #print(wget_command)
            command_output = subprocess.check_output(wget_command, stderr=subprocess.PIPE, shell=True)
            got_status = True

#            print("got status of %s %s in %s" % (url, station, savename_temp))
        except:
            print("can't connect to %s %s" % (url, station))
            line = stations_file.readline().rstrip()
            continue

        if os.path.exists(savename_temp):
            index_file_temp = open(savename_temp)

            index_line_temp = index_file_temp.readline().rstrip()
            #print("index_line_temp = %s" % index_line_temp)
        else:
            index_line_temp = ""

        if os.path.exists(savename) and os.path.getsize(savename) > 0:
            backup_file_name = "%s_index.backup.html" % (station)
            backup_file = os.path.join(path, backup_file_name)
              #            os.remove(backup_file)
            if os.path.exists(backup_file):
                os.remove(backup_file)
                try:
                   shutil.move(savename, backup_file)
                    #                    os.replace(savename, backup_file)
                except Exception as e:
                    print(f"Error moving {savename} to {backup_file}: {e}")
            else:
                shutil.move(savename, backup_file)
            #                os.rename(savename, backup_file)
        elif os.path.exists(savename) and os.path.getsize(savename) == 0:
            os.remove(savename)

        while index_line_temp != "":
            index_temp_start = index_line_temp.find("<script ")
            index_temp_stop = index_line_temp.find("</script>")
            if index_temp_start >= 0 and index_temp_stop >= 0:
                start = index_line_temp[0:index_temp_start]
                stop = index_line_temp[index_temp_stop+9:len(index_line_temp)]
                index_line = "%s%s" % (start, stop)
                #print(index_line)
                index_file = open(savename, "w")
                index_file.write(index_line)
                print("got status of %s %s in %s" % (url, station, savename))
                index_file.close()
            index_line_temp = index_file_temp.readline().rstrip()
        if os.path.exists(savename_temp):
            index_file_temp.close()
            os.remove(savename_temp)



        #try:
            #filename = wget.download(url, out=savename)

        #filename = savename
        if got_status:
            wget_seed_time_process(url, station, path, n_try, timeout)


        line = stations_file.readline().rstrip()


if __name__ == "__main__":
    main()
