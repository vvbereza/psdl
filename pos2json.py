#!/usr/bin/env python3

from optparse import OptionParser
import  json

def main():
    usage = "usage: %prog -d 'directory with files in json format'\
     -a 'IP address of ARD with port' -s 'ARD name' -p 'Position'"
    parser = OptionParser(usage)
    parser.add_option("-d", "--dir", dest="path", default=".",
                          help="PATH for files in json format")
    parser.add_option("-a", "--address", dest="address", default="localhost:80",
                          help="Address of ARD with port, default = 'localhost:80'")
    parser.add_option("-s", "--ardname", dest="ardname",
                          help="ARD name")
    parser.add_option("-p", "--position", dest="position",
                      help="Position to set to")

    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")

    (options, args) = parser.parse_args()

    process(options.path, options.address, options.ardname, options.position, options.verbose)

def process(path, address , ardname, position, verbose):
    import os


    #print(file, path, template, psdl, verbose)
    json_dir = ""
    file_name_path  = ""
    address_sploited = address.split(':')
    if len(address_sploited) > 1:
        ipaddress = address_sploited[0]
        port = address_sploited[1]
    elif len(address_sploited) == 1:
        ipaddress = address_sploited[0]
        port = '80'
    else:
        print("Wrong address of ARD provided")
        return
    if ipaddress != 'localhost':
        ipaddress_splitted = ipaddress.split('.')
        file_name_path = "%s_%s_%s_%s_%s_%s.json" % \
               (ardname, ipaddress_splitted[0], ipaddress_splitted[1], ipaddress_splitted[2], ipaddress_splitted[3], port)
    else:
        file_name_path  = "%s_%s_%s.json" % (ardname, ipaddress, port)
    file_name_path = os.path.join(path, file_name_path)

    json_dir = file_name_path
    if json_dir and os.path.exists(json_dir):
        with open(json_dir, 'r') as f:
            json_dir_lines = f.readlines()
            f.close()
        out_lines = []
        for json_dir_line in json_dir_lines:
            json_dir_line = json_dir_line.rstrip()
            if json_dir_line.find('Position') >= 0:
                position_line = json_dir_line.split(':')
                json_dir_line = "%s: \"%s\",\n" % (position_line[0], position)
                out_lines.append(json_dir_line)
                #print(json_dir_line)
            else:
                out_lines.append(json_dir_line)
                out_lines.append("\n")
                #print(json_dir_line)
#        print(out_lines)
        with open(json_dir, 'w') as f:
            f.writelines(out_lines)
            f.close()
    else:
        print("%s does not exist" % json_dir)



if __name__ == "__main__":
    main()
