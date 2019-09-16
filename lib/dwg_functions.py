import os
import re
import sys
import ntpath
import math

import itertools

def copy_files_from_list(from_dir="", to_dir="", file_list=""):
    if len(file_list) > 0:
        with open(file_list) as fl:
            files = fl.readlines()
            files = [line.rstrip('\n') for line in open(files)]




def compare_new_revs(dir1="", dir2=""):
    #rtn_list = ["CA123456", "CA123457", "CA123458", "CA123459"]
    files = os.listdir(dir1)
    cfiles = os.listdir(dir2)
    rtn_list = []
    for file in files:
        try:
            fsp = file.split('.')
            dwg_ext = fsp[-1]
            dwg_fn = fsp[0].upper().split('_')
            dwg_no = "".join(dwg_fn[:-1])
            print(file)
            dwg_rev = dwg_fn[-1]
            for cfile in cfiles:
                cfsp = cfile.split('.')
                cdwg_ext = cfsp[-1]
                cdwg_fn = cfsp[0].upper().split('_')
                cdwg_no = "".join(cdwg_fn[:-1])
                cdwg_rev = cdwg_fn[-1]
                if dwg_no == cdwg_no and dwg_ext == cdwg_ext and dwg_rev != cdwg_rev and min(dwg_rev,cdwg_rev) == cdwg_rev and not cfile in rtn_list:
                    rtn_list.append(file)
                    #if min(dwg_rev,cdwg_rev) == dwg_rev and not cfile in rtn_list:
                        #rtn_list.append(cfile)
                    #elif min(dwg_rev,cdwg_rev) == cdwg_rev and not file in rtn_list:
                        #rtn_list.append(file)
                    continue
        except Exception as e:
            print(repr(e) + '       ' + file)
            continue
    return rtn_list


def srch_superseded(srch_dir=""):
    files = os.listdir(srch_dir)
    rtn_list = []
    for file, cfile in itertools.combinations(files, 2):
    #compare(file, cfile)
    #for file in files:
        try:
            fsp = file.split('.')
            dwg_ext = fsp[-1]
            dwg_fn = fsp[0].upper().split('_')
            dwg_no = "".join(dwg_fn[:-1])
            dwg_rev = dwg_fn[-1]

            cfsp = cfile.split('.')
            cdwg_ext = cfsp[-1]
            cdwg_fn = cfsp[0].upper().split('_')
            cdwg_no = "".join(cdwg_fn[:-1])
            cdwg_rev = cdwg_fn[-1]

            if dwg_no == cdwg_no and dwg_ext == cdwg_ext and cdwg_rev != dwg_rev:
                if min(dwg_rev,cdwg_rev) == dwg_rev:
                    rtn_list.append(file)
                elif min(dwg_rev,cdwg_rev) == cdwg_rev:
                    rtn_list.append(cfile)
                #rtn_list.append( dwg_no + "_" + min(dwg_rev,cdwg_rev) + "." + str(dwg_ext))
                continue

        except Exception as e:
            print(repr(e) + '       ' + file)
            continue
    return rtn_list
