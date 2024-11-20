#!/usr/bin/env python3
import os
import shutil
import re
from optparse import OptionParser

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
    #  trying to add output with current configuration
    staname = input("\r\n0 - восстановить все группы\r\nДля какой группы будем менять конфигурацию (0,1,2,3)?:")
    loop = 0
    while True:
        remsta = ""
#        staname = input("\r\n0 - восстановить все группы\r\nДля какой группы будем менять конфигурацию (0,1,2,3)?:")
        if loop == -3:
            staname = input("\r\n0 - восстановить все группы\r\nДля какой группы будем менять конфигурацию (0,1,2,3)?:")
        while True:
            if staname == '1' or staname == '2' or staname == '3':
                break
            elif staname == '0' and loop == 0:
                print('Восстанавливаем все группы')
                if psdlini != tempini:
                    shutil.copy(tempini, psdlini)
                result3 = input("Надо ли менять или убирать ещё другую группу (Y/Д, y/д, N/Н или n/н)?:")
                if result3 == 'Y' or result3 == 'Д' or result3 == 'y' or result3 == 'д':
                    staname = input("\r\nДля какой группы будем менять конфигурацию (1,2,3)?:")
                    tempini = psdlini
                    loop = -3
                    break
                elif result3 == 'N' or result3 == 'Н' or result3 == 'n' or result3 == 'н':
                    loop = -2
                    break
            else:
                if loop == 0:
                    staname = input("Надо ввести  0,1,2 или 3):")
                else:
                    staname = input("Надо ввести  1,2 или 3):")
        if loop == -2:
            break
        remsta = input("Будем убирать всю группу (Y/Д,y/д или N/Н,n/н)?:")
        while True:
            if remsta == 'Y' or remsta == 'y' or  remsta == 'Д' or remsta == 'д' or remsta == 'N' \
                    or remsta == 'n' or remsta == 'Н' or remsta == 'н':
                break
            else:
                remsta = input("Надо ответить (Y/Д, y/д, N/Н или n/н):")
        if remsta == 'Y' or remsta == 'Д' or remsta == 'y' or remsta == 'д':
            with open(tempini) as f:
                lines = f.readlines()
                str = "{************ I0%sA" % staname
                if debug:
                    print(str)
                del_flg = False
            f.close()
            pattern = re.compile(re.escape(str))
            with open(psdlini, 'w') as f:
                for line in lines:
                    if debug:
                        print(line)
                    result = pattern.search(line)
                    if result:
                        del_flg = not del_flg
                    if debug:
                        print(del_flg)
                    if del_flg == False:
                        if debug:
                            print("write")
                        f.write(line)
            f.close()
        elif remsta == 'N' or remsta == 'n' or remsta == 'Н' or 'н':
            with open(tempini) as f:
                lines = f.readlines()
        #str = "Sensor=(StatName='I01A' SensName='BD2'"
            sensenum = input("\r\n0 - восстановить все АРД\r\nКакой АРД будем убирать из конфигурации (0,1,2,3,4)? :")
            while True:
                if sensenum == '1' or sensenum == '2' or sensenum == '3' or sensenum == '4':
                    break
                elif sensenum == '0':
                    #f.write(line)
                    print("Восстанавливаем все АРД")
                    break
                else:
                    sensenum = input("Надо ввести 0,1,2,3 или 4):")
            str = "Sensor=(StatName='I0%sA' SensName='BD%s'" % (staname, sensenum)
            PreCorrelateStr = "  PreCorrelate=( ('I0%sA" % staname
            del_flg = False
            pattern = re.compile(re.escape(str))
            if debug:
                print(pattern)
            PreCorrelatepattern = re.compile(re.escape(PreCorrelateStr))
            if debug:
                print(PreCorrelatepattern)
            with open(psdlini, 'w') as f:
                for line in lines:
                    if debug:
                        print(line)
                    result = pattern.search(line)
                    PreCorrelateresult = PreCorrelatepattern.search(line)
#                PreCorrelateresult = PreCorrelateStr.find(line)
                #print(PreCorrelateresult)
                    if result:
#               del_flg = not del_flg
                        del_flg = True
                    else:
                        del_flg = False
                    if debug:
                        print(del_flg)
                    if PreCorrelateresult:
                        if sensenum == '0':
                            line = "  PreCorrelate=( ('I0%sA:BD1' 'I0%sA:BD3') ('I0%sA:BD2' 'I0%sA:BD4') )\n" % (staname, staname, staname, staname)
                        elif sensenum == '1':
                            line = "  PreCorrelate=( ('I0%sA:BD2' 'I0%sA:BD3') ('I0%sA:BD2' 'I0%sA:BD4') )\n" % (staname,staname, staname, staname)
                        elif sensenum == '2':
                            line = "  PreCorrelate=( ('I0%sA:BD1' 'I0%sA:BD3') ('I0%sA:BD3' 'I0%sA:BD4') )\n" % (staname,staname, staname, staname)
                        elif sensenum == '3':
                            line = "  PreCorrelate=( ('I0%sA:BD1' 'I0%sA:BD2') ('I0%sA:BD2' 'I0%sA:BD4') )\n" % (staname,staname, staname, staname)
                        elif sensenum == '4':
                            line = "  PreCorrelate=( ('I0%sA:BD1' 'I0%sA:BD3') ('I0%sA:BD2' 'I0%sA:BD3') )\n" % (staname,staname, staname, staname)
                        if debug:
                            print(line)
                    if del_flg == False or sensenum == '0':
                        if debug:
                            print("write")
                        f.write(line)
            f.close()
        f.close()
        result2 =  input("Надо ли менять или убирать ещё другую группу (Y/Д, y/д, N/Н или n/н)?:")
        if result2 == 'Y' or result2 == 'Д' or result2 == 'y' or result2 == 'д':
            staname = input("\r\nДля какой группы будем менять конфигурацию (1,2,3)?:")
            tempini = psdlini
            loop += 1
            continue
        elif result2 == 'N' or result2 == 'Н' or result2 == 'n' or result2 == 'н':
            break

if __name__ == "__main__":
    main()
