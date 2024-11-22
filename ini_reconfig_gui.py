#!/usr/bin/env python3
import os
import shutil
import re
from optparse import OptionParser
import tkinter as tk

def main():
    usage = "usage: %prog -i 'stations.ini' -t 'PSDL template ini file' -p 'PSDL ini file'"
    parser = OptionParser(usage)
    parser.add_option("-i", "--file", dest="stations_file", default="stations.ini",
                      help="file with LIST of stations with IP addresses")
    parser.add_option("-t", "--tempini", dest="tempini", default="psdl.ini",
                          help="PSDL template ini file with full or relative path, default is psdl.ini")
    parser.add_option("-p", "--psdlini", dest="psdlini", default="psdl.ini",
                          help="PSDL ini file with full or relative path, default is psdl.ini")

    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("--debug",
                      action="store_true", dest="debug")

    (options, args) = parser.parse_args()

    process(options.stations_file, options.tempini, options.psdlini, options.verbose, options.debug)

def process(file, tempini, psdlini, verbose, debug):
    root = tk.Tk()
    root.title('Ini_reconfig_gui')
    tk.Label(root, text="Select ARD to reconfigure").pack()
    group_dict = {}
    station_dict = {}
    nsta = 0
    with open(file, 'r') as f:
        stations_lines = f.readlines()
        f.close()
    for line in stations_lines:
        line = line.rstrip()
        if line.find('#') == 0:
            continue
#        print(line)
        nsta += 1
        line_splitted = line.split()
        group = line_splitted[1][0:4]
        station = line_splitted[1]
        station_dict[nsta] = station
        group_dict.update({nsta:group})
        station_dict.update({nsta:station})
#    print(group_dict)
#    print(station_dict)
    nkey = 0
    grid = 0
    col = 0
    frame = tk.Frame(root)
    for key in group_dict:
        nkey += 1
#        print(nkey, key)
#        print(station_dict[key], end=" ")
        tk.Checkbutton(frame, text=station_dict[key]).grid(row=grid, column=col)
        col += 1
#        frame.pack()
        if  nkey % 4 == 0:
            tk.Checkbutton(frame, text=group_dict[key]).grid(row=grid, column=col)
            grid += 1
            col = 0
#            print(nkey, group_dict[key])
#            col += 1
#            print(station_dict[key])
#            tk.Checkbutton(frame, text=station_dict[key]).grid(row=grid, column=col)

#            frame = tk.Frame(root)
#            tk.Label(frame, text=group_dict[key]).pack()
#            tk.Label(frame, text=station_dict[key]).pack(side='bottom')
#            frame.pack()
#            print(": %s" %group_dict[key])
    grid += 1
    tk.Button(frame, text='Save' ).grid(row=grid, column=2)
    frame.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
