import os
import re
import sys

import tkinter as tk
from tkinter import filedialog
import ntpath

root = tk.Tk()
root.withdraw()

workdir = filedialog.askdirectory()
compdir = filedialog.askdirectory()
print("Find drawings with revisions")
os.chdir(workdir)
files = os.listdir()
compfiles = os.listdir(compdir)

def main():
    counter = 0;
    for file in files:
        try:
            fsp = file.split('.')
            dwg_ext = fsp[-1]
            dwg_fn = fsp[0].upper().split('_')
            dwg_no = dwg_fn[:-1]
            dwg_rev = dwg_fn[-1]
            for cfile in compfiles:
                cfsp = cfile.split('.')
                cdwg_ext = cfsp[-1]
                cdwg_fn = cfsp[0].upper().split('_')
                cdwg_no = cdwg_fn[:-1]
                cdwg_rev = cdwg_fn[-1]
                if dwg_no == cdwg_no and dwg_ext == cdwg_ext and cdwg_rev != dwg_rev:
                    print(str(dwg_no[0]) + "." + str(dwg_ext) + " has revisions " + dwg_rev + " and " + cdwg_rev)
                    continue
                     
        except Exception as e:
            #print(repr(e) + '       ' + file)
            continue
					 
    #print('Renamed ' + str(counter) + ' files in ' + workdir)
    input("Press Enter to exit...")

main()
