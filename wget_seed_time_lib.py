#!/usr/bin/env python3


def wget_seed_time_process(url, station, path, n_try, timeout):
    import os
    import subprocess
    import shutil

    index_name = "%s_seed_time.html" % station
    savename = os.path.join(path, index_name)


    if os.path.exists(savename) and os.path.getsize(savename) > 0:
         backup_file_name = "%s_seed_time.backup.html" % (station)
         backup_file = os.path.join(path, backup_file_name)
         if os.path.exists(backup_file):
            os.remove(backup_file)
            try:
                shutil.move(savename, backup_file)
#                os.replace(savename, backup_file)
            except Exception as e:
                print(f"Error moving {savename} to {backup_file}: {e}")
#         os.rename(savename, backup_file)
    elif os.path.exists(savename) and os.path.getsize(savename) == 0:
         os.remove(savename)

    try:
         wget_command = "wget %s/seed_time -t %s -T %s -O %s" % (url, n_try, timeout, savename)
         command_output = subprocess.check_output(wget_command, stderr=subprocess.PIPE, shell=True)
         print("got seedlink status of %s %s in %s" % (url, station, savename))
    except:
         print("can't connect to %s %s" % (url, station))