import os
import re
import sys
import ntpath
import math

import itertools


def srch_superseded(srch_dir=""):
    files = os.listdir(srch_dir)
    rtn_list = []
    counter = 0;
    stop_at = math.ceil(len(files)/2)
    for file, cfile in itertools.combinations(files, 2):
    #compare(file, cfile)
    #for file in files:
        try:
            fsp = file.split('.')
            dwg_ext = fsp[-1]
            dwg_fn = fsp[0].upper().split('_')
            dwg_no = dwg_fn[:-1]
            dwg_rev = dwg_fn[-1]
            cfsp = cfile.split('.')
            cdwg_ext = cfsp[-1]
            cdwg_fn = cfsp[0].upper().split('_')
            cdwg_no = cdwg_fn[:-1]
            cdwg_rev = cdwg_fn[-1]
            if dwg_no == cdwg_no and dwg_ext == cdwg_ext and cdwg_rev != dwg_rev:
                rtn_list.append( str(dwg_no[0]) + "_" + min(dwg_rev,cdwg_rev) + "." + str(dwg_ext))
                continue

        except Exception as e:
            #print(repr(e) + '       ' + file)
            continue
    return rtn_list
