#!/usr/bin/env python3

import os
from time import sleep



while True:
    try:
        #print(command1)
        #os.system(command1)
        command = "/home/sysop/PycharmProjects/infrapy/wget_html.py -i /home/sysop/PycharmProjects/infrapy/stations-I01A.ini -d /home/sysop/PycharmProjects/infrapy/html"
        os.system(command)
        command = "/home/sysop/PycharmProjects/infrapy/wget_html.py -i /home/sysop/PycharmProjects/infrapy/stations-I02A.ini -d /home/sysop/PycharmProjects/infrapy/html"
        os.system(command)
        command = "/home/sysop/PycharmProjects/infrapy/wget_html.py -i /home/sysop/PycharmProjects/infrapy/stations-I03A.ini -d /home/sysop/PycharmProjects/infrapy/html"
        os.system(command)
        command = "/home/sysop/PycharmProjects/infrapy/html2json-7.py -i /home/sysop/PycharmProjects/infrapy/stations-I01A.ini -d /home/sysop/PycharmProjects/infrapy/html -o /home/sysop/PycharmProjects/infrapy/status"
        os.system(command)
        command = "/home/sysop/PycharmProjects/infrapy/html2json-7.py -i /home/sysop/PycharmProjects/infrapy/stations-I02A.ini -d /home/sysop/PycharmProjects/infrapy/html -o /home/sysop/PycharmProjects/infrapy/status"
        os.system(command)
        command = "/home/sysop/PycharmProjects/infrapy/html2json-7.py -i /home/sysop/PycharmProjects/infrapy/stations-I03A.ini -d /home/sysop/PycharmProjects/infrapy/html -o /home/sysop/PycharmProjects/infrapy/status"
        os.system(command)
        command = "/home/sysop/PycharmProjects/infrapy/start_reg_A1.py -i /home/sysop/PycharmProjects/infrapy/stations-I01A.ini -d /home/sysop/PycharmProjects/infrapy/status"
        os.system(command)
        command = "/home/sysop/PycharmProjects/infrapy/start_reg_A1.py -i /home/sysop/PycharmProjects/infrapy/stations-I02A.ini -d /home/sysop/PycharmProjects/infrapy/status"
        os.system(command)
        command = "/home/sysop/PycharmProjects/infrapy/start_reg_A1.py -i /home/sysop/PycharmProjects/infrapy/stations-I03A.ini -d /home/sysop/PycharmProjects/infrapy/status"
        os.system(command)
        sleep(300)
    except KeyboardInterrupt:
        break
