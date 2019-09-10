import tkinter as tk
from tkinter import filedialog
from tkinter import *
import ntpath

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        #self.pack()

        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, pad=3)
        self.rowconfigure(0, pad=3)
        self.dir_1 = StringVar()
        self.dir1_choose = tk.Button(self).grid(row=0)
        self.dir1_choose["text"] = "Browse..."
        self.dir1_choose["command"] = self.choose_dir1

        #self.dir1_choose.pack(side="top")

        label1 = Label( root, textvariable = self.dir_1).grid(row=1)
        #label1.pack(side="left")

        self.dir_2 = StringVar()
        self.dir2_choose = tk.Button(self).grid(row=2,column=1)
        self.dir2_choose["text"] = "Browse..."
        self.dir2_choose["command"] = self.choose_dir2
        #self.dir2_choose.pack(side="top")

        label2 = Label( root, textvariable = self.dir_2).grid(row=2)
        #label2.pack(side="left")


        self.dir_print = tk.Button(self).grid(row=3)
        self.dir_print["text"] = "Print directory path"
        self.dir_print["command"] = self.print_dir
        self.dir_print.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy).grid(row=4)
        #self.quit.pack(side="bottom")

    def choose_dir1(self):
        self.dir_1.set(filedialog.askdirectory())

    def choose_dir2(self):
        self.dir_2.set(filedialog.askdirectory())
    
    def print_dir(self):
        print(self.dir_1)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
