
from tkinter import Tk, W, E, filedialog, StringVar
from tkinter.ttk import Frame, Button, Entry, Style, Label

class Example(Frame): 
    def __init__(self): 
        super().__init__() 
        self.initUI()
 
    def initUI(self):
        self.master.title("Drawing File Utility")
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')

        self.columnconfigure(0, pad=3) 
        self.rowconfigure(0, pad=3)

        # variable for first directory path
        self.dir_1 = StringVar()
        self.dir_1.set("directory one")

        self.dir1_choose = Button(self, text="Browse...")
        self.dir1_choose.grid(row=0, column=1)
        self.dir1_choose["command"] = self.choose_dir1
        
        label1 = Label(self, textvariable = self.dir_1)
        label1.grid(row=0, column=0)

        # variable for second directory path
        self.dir_2 = StringVar()
        self.dir_2.set("directory one")
        
        self.dir2_choose = Button(self, text="Browse...")
        self.dir2_choose.grid(row=1,column=1)
        self.dir2_choose["command"] = self.choose_dir2  

        label2 = Label(self, textvariable = self.dir_2)
        label2.grid(row=1, column=0)
 
        #self.dir_print = Button(self) 
        #self.dir_print["text"] = "Print directory path" 
        #self.dir_print["command"] = self.print_dir
        #self.dir_print.grid(row=3)
        #self.dir_print.pack(side="top") 
 
        self.quit = Button(self, text="QUIT", command=self.master.destroy)
        self.quit.grid(row=4)
        self.pack()
 
    def choose_dir1(self): 
        self.dir_1.set(filedialog.askdirectory()) 
 
    def choose_dir2(self):
        self.dir_2.set(filedialog.askdirectory()) 
     
    #def print_dir(self): 
        #print(self.dir_1)

def main():
    root = Tk() 
    app = Example() 
    app.mainloop()

main()
