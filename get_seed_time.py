#!/usr/bin/env python3

from optparse import OptionParser
#import wget
from html.parser import HTMLParser
import  json
import urllib
from urllib.request import urlopen
import re

import time, datetime, sys
import subprocess
from  subprocess import PIPE, Popen, run


def get_seed_time_process(file, path, sta):
    import string
    import re
    import os
    from obspy import  UTCDateTime
    from datetime import timezone
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
        station = station_line[1]
        #print(station)

        #print(json_filename)
        prev_navstat_json = {}
        prev_coords_json = {}
        prev_lon_json = {}
        prev_lat_json = {}
        prev_gps_status_json = {}
        gps_status_json = {}
        index_file_exist  = {}
        status = {}
        #print(json_dir)

        index_name = "%s_seed_time.html" % station
        index_path = os.path.join(path, index_name)
        #print(index_path)

        if sta == station and os.path.exists(index_path):
            index_file = open(index_path)
            index_line = index_file.readline().rstrip()
        #print(len(index_line))
            if len(index_line) == 0:
                #line = stations_file.readline().rstrip()
                index_file_exist[station] = False
            else:
                index_file_exist[station] = True
            index_file.close()
        else:
            index_file_exist[station] = False

        seed_date_json = {}
        seed_time_json = {}
        station_json = {}
        channels_json = {}
        #print("json file does not exist")

        #print("index_path = %s" % index_path)
#        if os.path.exists(index_path):
        index_line = ""
        if sta == station and index_file_exist[station] and os.path.getsize(index_path) != 0:
                index_file = open(index_path)
                index_line = index_file.readline().rstrip()
                if index_line != "":
                    #print("index_line_0 = %s" % index_line)
                    index_station = index_line.find('title')
                    index_line_splitted = index_line[index_station:].split()
                    #print(index_line_splitted[0])
                    station_splitted = index_line_splitted[0].split('>')
                    station_json['Station'] = station_splitted[1]
                    #print(station_splitted[1])
                index_line = index_file.readline().rstrip()
        elif sta == station and index_file_exist[station] and os.path.getsize(index_path) == 0:
            return -1
#        if len(index_line) == 0:
#            return -1


        channels_json = {}
        power_dict = {}
        while (index_line != ""):
            #print(index_line)
            #index = index_line.find('title')
            #if index:
            #    index_line = index_file.readline().rstrip()
            stat = ""
            index = index_line.find('last time of transfering SEED data:')
            #print(index_line)
            index_seedlink = index_line.find('SEED link client is not connected')
            if index_seedlink >= 0:
                station_html = index_line[index:index + 70]
                #print(station_html)
                return -2
            index_seedlink_not_started = index_line.find('SEED link server not started')
            if index_seedlink_not_started >= 0:
                #print("seedlink_not_started")
                return -2
            if index >= 0:
                station_html = index_line[index:index + 55]
                #station_json['Station'] = station_html
                seed_time_json_splitted = station_html.split()
                #station_json['Station'] = seed_time_json_splitted[1][:-1]
                #print(station_html)
                #print(seed_time_json_splitted)
                #print(seed_time_json_splitted[6])
                seed_date_json['Station'] = seed_time_json_splitted[6]
                seed_time_json['Station'] = seed_time_json_splitted[7]
                seed_date_splitted = seed_date_json['Station'].split('-')
                seed_time_splitted = seed_time_json['Station'].split(':')
                #print(seed_date_splitted, seed_time_splitted)
                year = seed_date_splitted[0]
                mon = seed_date_splitted[1]
                day = seed_date_splitted[2]
                hour = seed_time_splitted[0]
                min = seed_time_splitted[1]
                sec = seed_time_splitted[2]
                #print(seed_time_json_splitted)
                #print(station_json['Station'], seed_date_json['Station'], seed_time_json['Station'])
                #print(seed_date_splitted)
                #print(seed_time_splitted)
                stime_string = "%s-%s-%sT%s:%s:%s" % (year, mon, day, hour, min, sec)
                #print(stime_string)
                #print(stime)
                element = datetime.datetime(int(year), int(mon), int(day), int(hour), int(min), int(sec), tzinfo=timezone.utc)
                stime_timestamp = datetime.datetime.timestamp(element)
                #print(element, stime_timestamp)
                utc_timestamp = datetime.datetime.now(timezone.utc)
                utc_timestamp_now = datetime.datetime.now(timezone.utc).timestamp()
                seed_time_latency = utc_timestamp_now - stime_timestamp
                #print(utc_timestamp, utc_timestamp_now)
                #print(seed_time_latency)
                #print("before return:", station_json['Station'], stime_string, stime_timestamp, seed_time_latency)
                #print("latency = %s" % seed_time_latency)
                return seed_time_latency
            else:
                print(index, index_line)
                #print("latency = -1")
                return -1

        line = stations_file.readline().rstrip()