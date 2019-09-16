import os
import re
import sys

import tkinter as tk
from tkinter import filedialog
import ntpath

root = tk.Tk()
root.withdraw()

workdir = filedialog.askdirectory()

# CAE dwg numbers defined as ALPHA PREFIX | SERIAL NUM | TAB NUM | TYPE CODE | FAMILY GROUP
# File names we have are something like ALPHA PREFIX | SERIAL | TAB NUM | TYPE (FD or PL) | REVISION but are not consistent

# Desired format is SERIAL NUM | TAB NUM | TYPE | REV
# ex. ma399477_10_A_pl.pdf will read MA399477_10_PL_A.pdf after running this script.

# Do not remove the "r" from the front of the string and no trailing backslash. 
# Enter just like this: r'C:\Users\You\path\to\files'

#print("CAE drawing file renaming tool")
#print("Select directory containing filenames to be fixed")
#text = input("Enter directory: ")
valid_prefixes = ['CA','MA','PS','WD','TS','UD','MD','FP','ED','CD','PD']
valid_filetypes = ['pdf','dgn','dwg','dxf','xls','xlsx']

os.chdir(workdir)
print(os.getcwd())
input("Press Enter to continue or Ctrl+C to abort")
files = os.listdir()

def main():
    counter = 0;
    for file in files:
        try:
            fsp = file.split('.')
            dwg_no = fsp[0].upper()
            dwg_sp = dwg_no.split('_')

            # FILETYPE
            fn_ext = None

            if fsp[1].lower() in valid_filetypes:
                fn_ext = fsp[1].lower()
            else:
                raise Exception( 'Filetype not valid' )
        
            # ALPHA PREFIX

            base = None            
            alpha = dwg_sp[0][:2]
            if alpha in valid_prefixes:
                base = dwg_sp[0]
            else:
                raise Exception('Alpha prefix not valid')
     
            # TAB NUMBER
         
            tab = None
            for s in dwg_sp[1:]:
                if re.search("\d{2}", s):
                    tab = s
                
            # TYPE (PARTS LIST or FD)
            type = None
            for s in dwg_sp[1:]:
                if s == 'FD' or s == 'PL':
                    type = s
                    
            # REVISION
            rev = None
            for s in dwg_sp[1:]:
                if (len(s) == 1 or len(s) == 2) and (re.search("[A-Z]", s) or re.search("[A-Z]{2}", s) or s == '-') and (s != 'FD' and s != 'PL'):
                    rev = s
                elif len(s) == 1 and s == '0':
                    rev = '-'
 
            if(base and tab and type and rev and fn_ext):
                new_fn = base + '_' + tab + '_' + type + '_' + rev + '.' + fn_ext
                #print(new_fn)
            try:
                if new_fn != file:
                    os.rename(file, new_fn)
                    #print(file + '   -->   ' + new_fn)
                    counter += 1
            except:
                continue

        except Exception as e:
            if dwg_no and fn_ext and fn_ext in valid_filetypes:
                new_fn = dwg_no + '.' + fn_ext
                os.rename(file, new_fn)
            #print(repr(e) + '       ' + file)
            continue
                     
    print('Renamed ' + str(counter) + ' files in ' + workdir)
    input("Press Enter to exit...")

main()
