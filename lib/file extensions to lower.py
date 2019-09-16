import os
import re
import sys

import tkinter as tk
from tkinter import filedialog
import ntpath

root = tk.Tk()
root.withdraw()

workdir = filedialog.askdirectory()

#print("Filenames to lower")
#text = input("Enter directory: ")
#workdir = text

os.chdir(workdir)
print(os.getcwd())
input("Press Enter to continue")
files = os.listdir()

def main():
    counter = 0;
    for file in files:
        try:
            fsp = file.split('.')
            new_fn = fsp[0].upper() + '.' + fsp[1].lower()
            print(new_fn)
            os.rename(file, new_fn)
        except Exception as e:
            print(repr(e) + '       ' + file)
            continue

main()
