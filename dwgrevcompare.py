
from tkinter import Tk, W, E, filedialog, StringVar, LabelFrame, Listbox
from tkinter.ttk import Frame, Button, Entry, Style, Label
from my_dwg_utils import *


class Example(Frame): 
    def __init__(self): 
        super().__init__() 
        self.initUI()
 
    def initUI(self):
        self.master.title("Drawing File Utility")
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')

        self.columnconfigure(0, pad=3) 
        self.rowconfigure(0, pad=3)

        # Search a directory of drawing files to see if there are any superseded
        grp_sup_srch = LabelFrame(self.master, text="Revision compare")
        grp_sup_srch.grid(row=0, column=0)


        # variable for first directory path
        self.s_dir1 = StringVar()
        self.s_dir1.set(r"C:\Users\Colin\Documents\Code Projects\custom_file_utils\test_files")

        btn_dir1_choose = Button(grp_sup_srch, text="Browse...", command=self.choose_dir1)
        btn_dir1_choose.grid(row=0, column=0)
        #btn_dir1_choose["command"] = self.choose_dir1
        
        label1 = Label(grp_sup_srch, textvariable = self.s_dir1)
        label1.grid(row=0, column=1)

        self.lstbx_sup = Listbox(grp_sup_srch)
        self.lstbx_sup.grid(row=0, column=2)

        btn_srch = Button(grp_sup_srch, text="Search", command=self.exec_srch)
        btn_srch.grid(row=1, column=0)

        # variable for second directory path
        #self.s_dir2 = StringVar()
        #self.s_dir2.set("directory one")
        
        #btn_dir2_choose = Button(self, text="Browse...")
        #btn_dir2_choose.grid(row=1,column=1)
        #btn_dir2_choose["command"] = self.choose_dir2  

        #label2 = Label(self, textvariable = self.s_dir2)
        #label2.grid(row=1, column=0)
 
        #self.dir_print = Button(self) 
        #self.dir_print["text"] = "Print directory path" 
        #self.dir_print["command"] = self.print_dir
        #self.dir_print.grid(row=3)
        #self.dir_print.pack(side="top") 
 
        self.quit = Button(self, text="QUIT", command=self.master.destroy)
        self.quit.grid(row=4)
        #self.pack()
 
    def choose_dir1(self): 
        self.s_dir1.set(filedialog.askdirectory()) 
 
    def choose_dir2(self):
        self.s_dir2.set(filedialog.askdirectory())

    def exec_srch(self): 
        fl = srch_superseded(self.s_dir1.get())
        for f in fl:
            self.lstbx_sup.insert("end", f)

    #def print_dir(self): 
        #print(self.s_dir1)

def main():
    root = Tk() 
    root.geometry("640x480")
    app = Example() 
    app.mainloop()

main()
