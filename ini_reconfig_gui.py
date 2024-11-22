#!/usr/bin/env python3
import os
import shutil
import re
from optparse import OptionParser
import tkinter as tk

def main():
    usage = "usage: %prog -t 'PSDL template ini file' -p 'PSDL ini file'"
    parser = OptionParser(usage)
    parser.add_option("-t", "--tempini", dest="tempini", default="psdl.ini",
                          help="PSDL template ini file with full or relative path, default is psdl.ini")
    parser.add_option("-p", "--psdlini", dest="psdlini", default="psdl.ini",
                          help="PSDL ini file with full or relative path, default is psdl.ini")

    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("--debug",
                      action="store_true", dest="debug")

    (options, args) = parser.parse_args()

    process(options.tempini, options.psdlini, options.verbose, options.debug)

def process(tempini, psdlini, verbose, debug):
    root = tk.Tk()
    root.mainloop()

if __name__ == "__main__":
    main()
