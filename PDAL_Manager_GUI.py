
from tkinter import Tk, W, E, filedialog, StringVar, LabelFrame, Listbox, Menu
from tkinter.ttk import Frame, Button, Entry, Style, Label
from lib.dwg_functions import *
from lib.BPL_utils import *
from shutil import copyfile
import os, stat, ntpath


class Example(Frame):

    # top level directory containing PDAL
    
    
    def __init__(self): 
        super().__init__() 
        self.initUI()
 
    def initUI(self):
        self.master.title("SOFASTe PDAL Manager")

        # Menu Bar
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # File Menu
        file = Menu(menu, tearoff=0)
        file.add_command(label="Open PDAL", command=self.open_pdal)
        # add File Menu to Menu Bar
        menu.add_cascade(label="File", menu=file)

        # Tools Menu
        edit = Menu(menu, tearoff=0)
        edit.add_command(label="Scan for PDFs", command=self.pdfs_exist)
        edit.add_command(label="Remove .bak files", command=self.remove_bak)
        edit.add_command(label="Scan for superseded", command=self.find_superseded)
        edit.add_command(label="Scan CAE filenames", command=self.CAE_filenames_valid)
        # Add Validate Menu to Menu Bar
        menu.add_cascade(label="Tools", menu=edit)

        # Help Menu
        helpmenu = Menu(menu, tearoff=0)
        helpmenu.add_command(label="How to", command=self.howto_popup)
        menu.add_cascade(label="Help",menu=helpmenu)

        
        # Style and padding
        Style().configure("TButton", padding=(3, 5, 3, 5), font='serif 10')
        self.columnconfigure(0, pad=3) 
        self.rowconfigure(0, pad=3)



        # Widget variables
        # Full path to PDAL
        self.pdal_dir = StringVar()
               
        # Name of PDAL TLD
        self.pdal_name = StringVar()
        self.pdal_name.set("No PDAL selected")

        # Listbox for drawing filenames
        self.lstbox_lbl = StringVar()
        self.lstbox_lbl.set("Files:")
        self.lstbox_export_fn = "export.txt"

        # Full path to cable CSV file
        self.cable_csv_path = StringVar()
        self.cable_csv_path.set("No CSV file selected")
        # Cable assy dwg number
        self.cable_assy_num = StringVar()
        self.cable_assy_num.set("No cable labels")



        # Configure the main widget group
        grp_main = LabelFrame(self.master, text="PDAL")
        grp_main.grid(row=0, column=0)
        grp_main.config(padx=50, pady=20)

        # PDAL directory
        self.pdal_dir.set(r"C:\\")
        label_pdal_name = Label(grp_main, textvariable = self.pdal_name, width=40)
        label_pdal_name.grid(row=0, column=1)
        # Listbox
        lstbx_files_lbl = Label(grp_main, textvariable = self.lstbox_lbl)
        lstbx_files_lbl.grid(row=0, column=2)
        self.lstbx_files = Listbox(grp_main, selectmode="extended", width=80)
        self.lstbx_files.grid(row=1, column=2)
        btn_export_lstbx = Button(grp_main, text="Export Listbox", command=self.export_listbox)
        btn_export_lstbx.grid(row=2, column=2)

        # debug set PDAL directory
        #self.pdal_dir.set(r"C:\Users\Csullivan\Desktop\razor_work\!PDAL\mh47-2_pdal\submissions\ver_1.3\MH-47-2_PDAL")
        #os.chdir(r"C:\Users\Csullivan\Desktop\razor_work\!PDAL\mh47-2_pdal\submissions\ver_1.3\MH-47-2_PDAL")
        self.pdal_name.set("Choose PDAL")



        # Configure the cable labels widget group
        grp_cbllbl = LabelFrame(self.master, text="Cable Labels")
        grp_cbllbl.grid(row=1, column=0)
        grp_cbllbl.config(padx=50, pady=20)
        
        # Cable label file path
        cable_label_file = Label(grp_cbllbl, textvariable = self.cable_csv_path, width=40)
        cable_label_file.grid(row=0, column=0)
        btn_open_cable_csv = Button(grp_cbllbl, text="Open cable label CSV", command=self.open_cable_csv)
        btn_open_cable_csv.grid(row=1, column=0)

        # Cable Label Listbox
        lstbx_cables_lbl = Label(grp_cbllbl, textvariable = self.cable_assy_num)
        lstbx_cables_lbl.grid(row=0, column=1)
        self.lstbx_cables = Listbox(grp_cbllbl, selectmode="extended", width=80)
        self.lstbx_cables.grid(row=1, column=1)
        
        btn_print_labels = Button(grp_cbllbl, text="Print labels", command=self.print_labels)
        btn_print_labels.grid(row=2, column=1)

        btn_quit = Button(self.master, text="Quit", command=self.master.destroy)
        btn_quit.grid(row=3, column=0)





    def open_pdal(self):
        m_dir = filedialog.askdirectory()
        os.chdir(m_dir)
        self.pdal_dir.set(m_dir)
        m_name = m_dir.split('/')
        m_name = m_name[-1]
        self.pdal_name.set(m_name)

    def CAE_filenames_valid(self):
        m_dir = filedialog.askdirectory()
        invalid = validate_CAE_filenames(m_dir)
        if (len(invalid)):
            self.lstbx_files.delete(0, "end")
            self.lstbox_lbl.set("Nonstandard CAE drawing numbers:")
            self.lstbox_export_fn = "nonstandard.txt"
            for fn in invalid:
                self.lstbx_files.insert("end", fn)

    def find_superseded(self):
        m_filename = "folders.txt"
        m_folders = ""
        try:
            m_folders = open(m_filename, "r")
        except:
            popupmsg("folders.txt not found")
        self.lstbx_files.delete(0, "end")
        for m_folder in m_folders:
            if m_folder[0] == "#":
                continue
            self.lstbox_lbl.set("Superseded files:")
            self.lstbox_export_fn = "superseded.txt"
            try:
                superseded = srch_superseded(m_folder.strip())
                if len(superseded) > 0:
                    for sup_f in superseded:
                        #print(fn)
                        self.lstbx_files.insert("end", m_folder + "\\" + sup_f)
            except:
                popupmsg("Encountered problem with " + m_folder)

    def pdfs_exist(self):
        m_filename = "folders.txt"
        m_folders = ""
        try:
            m_folders = open(m_filename, "r")
        except:
            popupmsg("folders.txt not found")
        self.lstbx_files.delete(0, "end")
        for m_f in m_folders:
            if m_f[0] == "#":
                continue
            #print(m_f.strip())
            self.lstbox_lbl.set("No PDFs found for:")
            self.lstbox_export_fn = "missing_pdfs.txt"
            try:
                no_pdfs = check_for_pdfs(m_f.strip())
                if len(no_pdfs) > 0:
                    for fn in no_pdfs:
                        #print(fn)
                        self.lstbx_files.insert("end", m_f + "\\" + fn)
            except:
                popupmsg("Encountered problem with " + m_f)

    def remove_bak(self):
        m_filename = "folders.txt"
        m_folders = ""
        try:
            m_folders = open(m_filename, "r")
        except:
            popupmsg("folders.txt not found")
        m_found = False
        self.lstbx_files.delete(0, "end")
        for m_f in m_folders:
            if m_f[0] == "#":
                continue
            try:
                m_baks = delete_bak_files(m_f.strip())
                if (len(m_baks) > 0):
                    self.lstbox_lbl.set(".bak files found and deleted:")
                    self.lstbox_export_fn = "deleted_baks.txt"
                    for bf in m_baks:
                        self.lstbx_files.insert("end", m_f + "\\" + bf)
            except:
                popupmsg("Encountered problem with " + m_f)
        if (not m_found):
            popupmsg("No .bak files found")

    def export_listbox(self):
        path = self.pdal_dir.get() + "\\" + self.lstbox_export_fn
        m_file = open(path, "w")
        for item in self.lstbx_files.get(0, "end"):
            m_file.write(item + "\n")
        m_file.close()
        popupmsg("Saved to " + path)


    def open_cable_csv(self):
        filepath = filedialog.askopenfilename()
        self.cable_csv_path.set(filepath)
        fp_sp = ntpath.split(filepath)
        filename = fp_sp[1]
        fn_sp = filename.split(".")
        self.cable_assy_num.set(fn_sp[0])
        f_csv = open(filepath, "r")
        for line in f_csv:
            self.lstbx_cables.insert("end", line)
            
    def print_labels(self):
        cbllbl_dir = self.cable_assy_num.get()
        if(not os.path.isdir(cbllbl_dir)):
            os.mkdir(cbllbl_dir)
        filepath = self.cable_csv_path.get()
        GenerateXMLinFives(cbllbl_dir, filepath)
        #self.lstbx_cables.insert("end", "Saved to " + filepath)
        #self.lstbx_cables.insert("end", "Ready to print...")
        lbl_files = os.listdir(cbllbl_dir)
        for f in lbl_files:
            SendToBP33(cbllbl_dir + "\\" + f, False)
            self.lstbx_cables.insert("end", "Sent " + f + " to printer")
        self.lstbx_cables.insert("end", "Finished!")
        
    def howto_popup(self):
        msg = "folders.txt file goes in top level directory. Each line \ncontains path to folder with native files. For example:\n"
        msg += "\nCAE\\Drawings"
        msg += "\nCAE\\Schematics"
        msg += "\nVEC\\assembly"
        popupmsg(msg)


def popupmsg(msg):
    popup = Tk()
    popup.wm_title("Message")
    label = Label(popup, text=msg, font='serif 10')
    label.pack(side="top", fill="x", padx=40, pady=20)
    B1 = Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def main():
    app = Example()
    app.mainloop()

main()
