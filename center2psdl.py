#!/usr/bin/env python3
import os
import shutil
import re
from optparse import OptionParser

def main():
    usage = "usage: %prog [-i 'PSDL ini file'] [--coord='lat,lon'] [--radius0='R0'] [-radius1='R1']"
    parser = OptionParser(usage)
    parser.add_option("-i", "--ini", dest="ini", default="psdl.ini",
                      help="PSDL  template ini file with full or relative path, default is psdl.ini")
    parser.add_option("--coord", dest="coord",
                      help="Coordinates(Fi0,Ld0) in form 'lat,lon'")
    parser.add_option("--radius0", dest="radius0",
                      help="Radius of cell(R0)'")
    parser.add_option("--radius1", dest="radius1",
                      help="Radius (R1)'")

    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("--debug",
                      action="store_true", dest="debug")

    (options, args) = parser.parse_args()

    process(options.ini, options.coord, options.radius0, options.radius1, options.verbose, options.debug)

def process(ini, coord, radius0, radius1, verbose, debug):
    str_Fi0 = "Fi0"
    str_Ld0 = "Ld0"
    str_R0 = "R0"
    str_R1 = "R1"
    pattern_Fi0 = re.compile(re.escape(str_Fi0))
    pattern_Ld0 = re.compile(re.escape(str_Ld0))
    pattern_R0 = re.compile(re.escape(str_R0))
    pattern_R1 = re.compile(re.escape(str_R1))
    Fi0 = Ld0 = R0 = R1 = ""
 #   if coord and radius0 and radius1:
    if coord:
        coord_splitted = coord.split(',')
        Fi0_new = coord_splitted[0]
        if debug:
            print(Fi0_new)
        Fi0_comment = ""
        Ld0_new = coord_splitted[1]
        if debug:
            print(Ld0_new)
        Ld0_comment = ""
        if radius0:
            R0_new = radius0
            R0_comment = ""
            if debug:
                print(R0_new)
        else:
            R0_new = ""
        if radius1:
            R1_new = radius1
            R1_comment = ""
            if debug:
                print(R1_new)
        else:
            R1_new = ""
        with open(ini) as f:
            lines = f.readlines()
            f.close()
    else:
        with open(ini) as f:
            lines = f.readlines()
            f.close()
        for line in lines:
            result_Fi0 = pattern_Fi0.search(line)
            if result_Fi0:
                line_Fi0_splitted = line.split('{')
                Fi0 = line_Fi0_splitted[0]
                Fi0_comment = ""
                if len(line_Fi0_splitted) > 1:
                    Fi0_comment = line_Fi0_splitted[1]
                    Fi0_comment = Fi0_comment.split('}')
                    Fi0_comment = Fi0_comment[0]
                print("\r\nТекущие координаты центра:")
                print(Fi0)
            result_Ld0 = pattern_Ld0.search(line)
            if result_Ld0:
                line_Ld0_splitted = line.split('{')
                Ld0 = line_Ld0_splitted[0]
                Ld0_comment = ""
                if len(line_Ld0_splitted) > 1:
                    Ld0_comment = line_Ld0_splitted[1]
                    Ld0_comment = Ld0_comment.split('}')
                    Ld0_comment = Ld0_comment[0]
                print(Ld0)

#            print(line)
            result_R0 = pattern_R0.search(line)
            if result_R0:
                line_R0_splitted = line.split('{')
                R0 = line_R0_splitted[0]
                R0_comment = ""
                if len(line_R0_splitted) > 1:
                    R0_comment = line_R0_splitted[1]
                    R0_comment = R0_comment.split('}')
                    R0_comment = R0_comment[0]
                print("Текущий радиус ячейки:")
                print(R0)
#            print(line)
            result_R1 = pattern_R1.search(line)
            if result_R1:
                line_R1_splitted = line.split('{')
                R1 = line_R1_splitted[0]
                R1_comment = ""
                if len(line_R1_splitted) > 1:
                    R1_comment = line_R1_splitted[1]
                    R1_comment = R1_comment.split('}')
                    R1_comment = R1_comment[0]
                print("Текущий радиус ассоциации:")
                print(R1)


        change_coord = input("Будем менять координаты центра (Y/Д,y/д или N/Н,n/н)?:")
        while True:
            if change_coord == 'Y' or change_coord == 'y' or change_coord == 'Д' or change_coord == 'д' or change_coord == 'N' \
                or change_coord == 'n' or change_coord == 'Н' or change_coord == 'н':
                break
            else:
                change_coord = input("Надо ответить (Y/Д, y/д, N/Н или n/н):")
        if change_coord == 'Y' or change_coord == 'Д' or change_coord == 'y' or change_coord == 'д':
        #print(Fi0)
        #print(Ld0)
        #print(R0)
        #print(R1)
            while(True):
                Fi0_new = input("\r\nВведите новую широту (Fi0):")
                try:
                    Fi0_new = float(Fi0_new)
                    break
                except ValueError:
                    print("Вы ввели не число, повторите")
                    continue

        #print(Fi0_new)
            while(True):
                Ld0_new = input("\r\nВведите новую долготу (Ld0):")
                try:
                    Ld0_new = float(Ld0_new)
                    break
                except ValueError:
                    print("Вы ввели не число, повторите")
                    continue

        #print(Ld0_new)

            while(True):
                R0_new = input("\r\nВведите новый радиус ячейки (R0):")
                try:
                    R0_new = float(R0_new)
                    break
                except ValueError:
                    print("Вы ввели не число, повторите")
                    continue
        #print(R0_new)

            while(True):
                R1_new = input("\r\nВведите новый радиус ассоциации (R1):")
                try:
                    R1_new = float(R1_new)
                    break
                except ValueError:
                    print("Вы ввели не число, повторите")
                    continue

        else:
            return
        #print(R1_new)
        f.close()
    with open(ini, 'w') as f:
        for line in lines:
            if debug:
                print(line)
            result_Fi0 = pattern_Fi0.search(line)
            if result_Fi0 and Fi0_new:
                if debug:
                    print(line)
                if Fi0_comment:
                    line = "  Fi0=%s {%s}\n" % (Fi0_new, Fi0_comment)
                else:
                    line = "  Fi0=%s\n" % (Fi0_new)

                if debug:
                    print(line)

            result_Ld0 = pattern_Ld0.search(line)
            if result_Ld0 and Ld0_new:
               if debug:
                    print(line)
               if Ld0_comment:
                    line = "  Ld0=%s {%s}\n" % (Ld0_new, Ld0_comment)
               else:
                    line = "  Ld0=%s\n" % (Ld0_new)

               if debug:
                   print(line)

            result_R0 = pattern_R0.search(line)
            if result_R0 and R0_new:
                 if debug:
                    print(line)
                 if R0_comment:
                    line = "  R0=%s {%s}\n" % (R0_new, R0_comment)
                 else:
                    line = "  R0=%s\n" % (R0_new)
                 if debug:
                    print(line)
            result_R1 = pattern_R1.search(line)
            if result_R1 and R1_new:
#                    if debug:
#                        print(line)
                  if R1_comment:
                     line = "  R1=%s {%s}\n" % (R1_new, R1_comment)
                  else:
                     line = "  R1=%s\n" % (R1_new)
                  if debug:
                     print(line)
            f.write(line)
    f.close()

if __name__ == "__main__":
    main()
