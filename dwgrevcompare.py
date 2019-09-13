
from tkinter import Tk, W, E, filedialog, StringVar, LabelFrame, Listbox
from tkinter.ttk import Frame, Button, Entry, Style, Label
from inc_dwg_utils import *


class Example(Frame): 
    def __init__(self): 
        super().__init__() 
        self.initUI()
 
    def initUI(self):
        self.master.title("Drawing File Utility")
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')

        self.columnconfigure(0, pad=3) 
        self.rowconfigure(0, pad=3)

        #
        # Search a directory of drawing files to see if there are any superseded
        #
        grp_sup_srch = LabelFrame(self.master, text="List old revisions")
        grp_sup_srch.grid(row=0, column=0)
        # variable for first directory path
        self.s_dir1 = StringVar()
        self.s_dir1.set(r".\test_files")
        btn_dir1_choose = Button(grp_sup_srch, text="Browse...", command=self.choose_dir1)
        btn_dir1_choose.grid(row=0, column=0)
        #btn_dir1_choose["command"] = self.choose_dir1
        label1 = Label(grp_sup_srch, textvariable = self.s_dir1, width=40)
        label1.grid(row=0, column=1)
        self.lstbx_sup = Listbox(grp_sup_srch, selectmode="extended")
        self.lstbx_sup.grid(row=0, column=2)
        btn_srch = Button(grp_sup_srch, text="Search", command=self.exec_srch)
        btn_srch.grid(row=1, column=0)


        #
        # Search a directory of drawing files to see if there are any superseded
        #
        grp_rev_cmp = LabelFrame(self.master, text="Compare directories for new revisions")
        grp_rev_cmp.grid(row=1, column=0)
        # variable for first directory path
        self.s_dir2 = StringVar()
        self.s_dir2.set("test_files_cmp1")
        self.s_dir3 = StringVar()
        self.s_dir3.set("test_files_cmp2")
        
        btn_dir2_choose = Button(grp_rev_cmp, text="Browse...")
        btn_dir2_choose.grid(row=0,column=0)
        btn_dir2_choose["command"] = self.choose_dir2  

        label2 = Label(grp_rev_cmp, textvariable = self.s_dir2, width=40)
        label2.grid(row=0, column=1)
        
        btn_dir3_choose = Button(grp_rev_cmp, text="Browse...")
        btn_dir3_choose.grid(row=1,column=0)
        btn_dir3_choose["command"] = self.choose_dir3  

        label3 = Label(grp_rev_cmp, textvariable = self.s_dir3, width=40)
        label3.grid(row=1, column=1)

        self.lstbx_cmp = Listbox(grp_rev_cmp, selectmode="extended")
        self.lstbx_cmp.grid(row=0, column=2)
 
        btn_cmp = Button(grp_rev_cmp, text="Compare", command=self.exec_cmp)
        btn_cmp.grid(row=2, column=0) 
 
        self.quit = Button(self.master, text="QUIT", command=self.master.destroy)
        self.quit.grid(row=4)
        #self.pack()
 
    def choose_dir1(self): 
        self.s_dir1.set(filedialog.askdirectory()) 
 
    def choose_dir2(self):
        self.s_dir2.set(filedialog.askdirectory())

    def choose_dir3(self):
        self.s_dir3.set(filedialog.askdirectory())

    def exec_srch(self): 
        fl = srch_superseded(self.s_dir1.get())
        for f in fl:
            self.lstbx_sup.insert("end", f)

    def exec_cmp(self): 
        fl = compare_new_revs(self.s_dir2.get(), self.s_dir3.get())
        for f in fl:
            self.lstbx_cmp.insert("end", f)

    #def print_dir(self): 
        #print(self.s_dir1)

def main():
    root = Tk() 
    root.geometry("640x480")
    app = Example() 
    app.mainloop()

main()
