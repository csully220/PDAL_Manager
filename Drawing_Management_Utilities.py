
from tkinter import Tk, W, E, filedialog, StringVar, LabelFrame, Listbox
from tkinter.ttk import Frame, Button, Entry, Style, Label
from lib.dwg_functions import *
from shutil import copyfile
import os, stat

class Example(Frame): 
    def __init__(self): 
        super().__init__() 
        self.initUI()
 
    def initUI(self):
        self.master.title("Drawing File Utility")
        Style().configure("TButton", padding=(3, 5, 3, 5), font='serif 10')

        self.columnconfigure(0, pad=3) 
        self.rowconfigure(0, pad=3)

        #
        # Search a directory of drawing files to see if there are any superseded
        #
        # Group - Scan directory and list old revisions
        grp_sup_srch = LabelFrame(self.master, text="Scan directory and list old revisions")
        grp_sup_srch.grid(row=0, column=0)
        grp_sup_srch.config(padx=50, pady=20)
        # Row 0
        # Path - directory
        self.s_dir1 = StringVar()
        self.s_dir1.set(r".\test_files")
        # Browse directory button
        btn_dir1_choose = Button(grp_sup_srch, text="Browse...", command=self.choose_dir1)
        btn_dir1_choose.grid(row=0, column=0)
        # Label - directory
        label1 = Label(grp_sup_srch, textvariable = self.s_dir1, width=40)
        label1.grid(row=0, column=1)
        # Row 1
        # Load file list button
        btn_load_list = Button(grp_sup_srch, text="Load from file", command=self.load_sup_file)
        btn_load_list.grid(row=1, column=0)
        # Listbox
        lstbx_sup_lbl = Label(grp_sup_srch, text = "Superseded drawings:")
        lstbx_sup_lbl.grid(row=0, column=2)
        self.lstbx_sup = Listbox(grp_sup_srch, selectmode="extended")
        self.lstbx_sup.grid(row=1, column=2)
        # Row 2
        grp_sup_srch.rowconfigure(2, pad=20)
        # Scan button
        btn_srch = Button(grp_sup_srch, text="Scan", command=self.sup_srch)
        btn_srch.grid(row=2, column=0)
        # Save button
        btn_save_sup = Button(grp_sup_srch, text="Save to file", command=self.save_superseded)
        btn_save_sup.grid(row=2, column=1)
        # Delete button
        btn_del_old = Button(grp_sup_srch, text="Delete files", command=self.delete_old)
        btn_del_old.grid(row=2, column=2)
        

        #
        # Search a directory of drawing files to see if there are any superseded
        #
        # Group - Compare two directories and list new revisions
        grp_rev_cmp = LabelFrame(self.master, text="Compare two directories and list new revisions")
        grp_rev_cmp.grid(row=1, column=0)
        grp_rev_cmp.config(padx=10, pady=20)
        # Path - first directory
        self.s_dir2 = StringVar()
        self.s_dir2.set(r".\test_files_src")
        # Path - second directory
        self.s_dir3 = StringVar()
        self.s_dir3.set(r".\test_files_tgt")
        # Row 0
        # Browse first directory button
        lbl_src_dir = Label(grp_rev_cmp, text = "New dwgs")
        lbl_src_dir.grid(row=0, column=0)
        btn_dir2_choose = Button(grp_rev_cmp, text="Set source dir", command=self.choose_dir2)
        btn_dir2_choose.grid(row=1,column=0)
        # Row 1
        # Label - first directory
        label2 = Label(grp_rev_cmp, textvariable = self.s_dir2, width=40)
        label2.grid(row=1, column=1)
        # Listbox - compare directories to find new revs
        lstbx_cmp_lbl = Label(grp_rev_cmp, text = "Found new revisions:")
        lstbx_cmp_lbl.grid(row=0, column=2)
        self.lstbx_cmp = Listbox(grp_rev_cmp, selectmode="extended")
        self.lstbx_cmp.grid(row=1, column=2)
        # Row 2
        # Browse second directory button
        lbl_tgt_dir = Label(grp_rev_cmp, text = "Current (old) dwgs")
        lbl_tgt_dir.grid(row=2, column=0)
        # Row 3
        btn_dir3_choose = Button(grp_rev_cmp, text="Set target dir", command=self.choose_dir3)
        btn_dir3_choose.grid(row=3,column=0)
        # Label - second directory
        label3 = Label(grp_rev_cmp, textvariable = self.s_dir3, width=40)
        label3.grid(row=3, column=1)
        # Row 4
        grp_rev_cmp.rowconfigure(4, pad=20)
        # Load file list button
        btn_load_cmp = Button(grp_rev_cmp, text="Load from file", command=self.load_cmp_file)
        btn_load_cmp.grid(row=4, column=0)
        # Row 5
        grp_rev_cmp.rowconfigure(5, pad=20)
        # Compare button
        btn_cmp = Button(grp_rev_cmp, text="Compare", command=self.cmp_srch)
        btn_cmp.grid(row=5, column=0)
        # Save button
        btn_save_cmp = Button(grp_rev_cmp, text="Save to file", command=self.save_new_revs)
        btn_save_cmp.grid(row=5, column=1)
        # Copy button
        btn_copy_cmp = Button(grp_rev_cmp, text="Copy files", command=self.copy_new)
        btn_copy_cmp.grid(row=5, column=2)

        #
        # Search a directory of drawing files to see if there are any superseded
        #
        # Group - Misc
        grp_misc = LabelFrame(self.master, text="Misc")
        grp_misc.grid(row=2, column=0)
        grp_misc.config(padx=10, pady=20)
        # Generate list of files
        btn_filelist = Button(grp_misc, text="Export directory contents to .txt", command=self.save_file_list)
        btn_filelist.grid(row=0, column=0)
        # Validate filenames
        btn_validate = Button(grp_misc, text="Validate CAE filenames", command=self.val_filenames)
        btn_validate.grid(row=0, column=1)
        # Check /pdf subdirectory for pdf corresponding to native files
        btn_verify_pdfs = Button(grp_misc, text="Check for PDFs", command=self.verify_pdfs)
        btn_verify_pdfs.grid(row=0, column=2)
        # Check /pdf subdirectory for pdf corresponding to native files
        btn_verify_pdf_dates = Button(grp_misc, text="Check PDF mod date", command=self.verify_pdf_dates)
        btn_verify_pdf_dates.grid(row=0, column=3)
        # Quit
        btn_quit = Button(self.master, text="Quit", command=self.master.destroy)
        btn_quit.grid(row=3, column=0)


    def choose_dir1(self): 
        self.s_dir1.set(filedialog.askdirectory()) 
 
    def choose_dir2(self):
        self.s_dir2.set(filedialog.askdirectory())

    def choose_dir3(self):
        self.s_dir3.set(filedialog.askdirectory())

    def sup_srch(self):
        self.lstbx_sup.delete(0, "end")
        fl = srch_superseded(self.s_dir1.get())
        for f in fl:
            self.lstbx_sup.insert("end", f)

    def load_sup_file(self):
        file_list = filedialog.askopenfilename()
        files = [line.rstrip('\n') for line in open(file_list)]
        for f in files:
            self.lstbx_sup.insert("end", f)

    def save_superseded(self):
        f_sup = open(self.s_dir1.get() + "\\superseded.txt", "w")
        for f in self.lstbx_sup.get(0, "end"):
            f_sup.write(f + "\n")
        f_sup.close()
        popupmsg("List saved to " + self.s_dir1.get() + "\\superseded.txt")

    def save_new_revs(self):
        f_sup = open(self.s_dir3.get() + "\\new_revs.txt", "w")
        for f in self.lstbx_cmp.get(0, "end"):
            f_sup.write(f + "\n")
        f_sup.close()
        popupmsg("List saved to " + self.s_dir3.get() + "\\new_revs.txt")

    def cmp_srch(self):
        self.lstbx_cmp.delete(0, "end")
        fl = compare_new_revs(self.s_dir2.get(), self.s_dir3.get())
        for f in fl:
            self.lstbx_cmp.insert("end", f)
        popupmsg("Found " + str(self.lstbx_cmp.size()) + " possible new revisions")

    def load_cmp_file(self):
        file_list = filedialog.askopenfilename()
        files = [line.rstrip('\n') for line in open(file_list)]
        for f in files:
            self.lstbx_cmp.insert("end", f)

    def copy_new(self): 
        fl = self.lstbx_cmp.get(0, "end")
        for f in fl:
            copyfile(self.s_dir2.get() + "\\" + f, self.s_dir3.get() + "\\" + f)

    def delete_old(self): 
        fl = self.lstbx_sup.get(0, "end")
        for f in fl:
            full_path = self.s_dir1.get() + "\\" + f
            if os.path.exists(full_path):
                try:
                    os.chmod(full_path, stat.S_IWRITE)
                    os.remove(full_path)
                    print("Removed " + full_path)
                except Exception as e:
                    print(repr(e))

    def save_file_list(self):
        file_dir = filedialog.askdirectory()
        files = os.listdir(file_dir)
        outfile = open(file_dir + "/file_list.txt", "w")
        for f in files:
            outfile.write(f + "\n")
        outfile.close()
        popupmsg("List saved to " + file_dir + "/file_list.txt")

    def verify_pdfs(self):
        no_pdfs = check_for_pdfs(filedialog.askdirectory())
        if len(no_pdfs) == 0:
            popupmsg("Found PDFs for all native files")
        else:
            msg_lbl = "Missing PDFs for:\n\n"
            for fn in no_pdfs:
                msg_lbl += fn + "\n"
            popupmsg(msg_lbl)

    def verify_pdf_dates(self):
        old_pdfs = check_for_old_pdfs(filedialog.askdirectory())
        if len(old_pdfs) == 0:
            popupmsg("All PDFs are current")
        else:
            msg_lbl = "Outdated PDFs:\n\n"
            for fn in old_pdfs:
                msg_lbl += fn + "\n"
            popupmsg(msg_lbl)


    def val_filenames(self):
        files = os.listdir(filedialog.askdirectory())
        for f in files:
            if not validate_CAE_filename(f):
                print(f)


def popupmsg(msg):
    popup = Tk()
    popup.wm_title("Message")
    label = Label(popup, text=msg, font='serif 10')
    label.pack(side="top", fill="x", padx=40, pady=20)
    B1 = Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def main():
    root = Tk() 
    #root.geometry("640x800")
    app = Example() 
    app.mainloop()

main()
