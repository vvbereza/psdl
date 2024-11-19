import os
from datetime import datetime, timezone
import re
from optparse import OptionParser

def main():
    usage = "usage: %prog -d 'PSDL directory'"
    parser = OptionParser(usage)
    parser.add_option("-d", "--dir", dest="dir", default=".",
                          help="PSDL directory with full or relative path, default is '.'")

    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("--debug",
                      action="store_true", dest="debug")

    (options, args) = parser.parse_args()

    process(options.dir, options.verbose, options.debug)

def process(dir, verbose, debug):

#    current_datetime = datetime.utcnow()
    current_datetime = datetime.now(timezone.utc)

    current_datetime_str = current_datetime.strftime('%Y %m %d %H %M %S')
    i01a_last_path = os.path.join(dir, 'I01A.last')
    i02a_last_path = os.path.join(dir, 'I02A.last')
    i03a_last_path = os.path.join(dir, 'I03A.last')
    if debug:
        print(current_datetime_str)
        print(i01a_last_path)
        print(i02a_last_path)
        print(i03a_last_path)
    with open(i01a_last_path, 'w') as f:
        f.write(current_datetime_str)
    with open(i02a_last_path, 'w') as f:
        f.write(current_datetime_str)
    with open(i03a_last_path, 'w') as f:
        f.write(current_datetime_str)

if __name__ == "__main__":
    main()
