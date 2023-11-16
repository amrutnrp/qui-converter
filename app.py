import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
import  subprocess, os


# from ctypes import windll
# windll.shcore.SetProcessDpiAwareness(1)

class MainApplication():
    def __init__(self):
        self.QMainWindow1 = tk.Tk()

        #=========congigure_gui ======================
        self.QMainWindow1.title("MainWindow")
        self.QMainWindow1.geometry("630x326")
        self.QMainWindow1.resizable(True, True)
        ##=========create_widgets ======================
        self.widget_items = {}
        style_obj = ttk.Style()
        self.checkbox_var = {}


        self.widget_items ["pushButton"] = ttk.Button( master = self.QMainWindow1,text='Browse .ui file',style='pushButton.TButton',)
        self.widget_items ["pushButton"].place(x = 20,y = 10,height=41,width=181, )
        style_obj.configure('pushButton.TButton', font=('MS Shell Dlg 2', 14) , )
        self.widget_items ["textEdit"] = scrolledtext.ScrolledText ( master = self.QMainWindow1,font=('MS Shell Dlg 2', 10),)
        self.widget_items ["textEdit"] .place(x = 210,y = 10,width = 391,height = 81,)
        self.widget_items ["label_2"] = ttk.Label(master = self.QMainWindow1,text = "Select Library ",style='label_2.TLabel',)
        self.widget_items ["label_2"] .place(x = 20,y = 50,height=41,width=150,)
        style_obj.configure('label_2.TLabel', font=('MS Shell Dlg 2', 14) , )
        options_comboBox = ["Tkinter","Dear PYGUI","PyFLTK","IUP C", "iup lua"]
        self.clicked_comboBox = tk.StringVar()
        self.clicked_comboBox.set( options_comboBox [1] )
        self.widget_items ["comboBox"] = tk.OptionMenu( self.QMainWindow1 , self.clicked_comboBox , *options_comboBox)

        self.widget_items ["comboBox"].place(x = 20,y = 90,height=31,width=181, )
        self.widget_items ["comboBox"].config(font = ('MS Shell Dlg 2', 12) ,)
        menu = self.QMainWindow1.nametowidget(self.widget_items ["comboBox"].menuname)
        menu.config(font=('MS Shell Dlg 2', 12) )

        self.widget_items ["pushButton_2"] = ttk.Button( master = self.QMainWindow1,text='Convert',style='pushButton_2.TButton',)
        self.widget_items ["pushButton_2"].place(x = 20,y = 130,height=161,width=181, )
        style_obj.configure('pushButton_2.TButton', font=('MS Shell Dlg 2', 14) , )
        self.widget_items ["textEdit_2"] = scrolledtext.ScrolledText ( master = self.QMainWindow1,font=('MS Shell Dlg 2', 10),)
        self.widget_items ["textEdit_2"] .place(x = 210,y = 100,width = 391,height = 191,)



    def show(self):
        self.QMainWindow1.mainloop()


class Processor():
    def __init__(self, GUI_obj):
        self.browse_btn = GUI_obj.widget_items ["pushButton"]
        self.cvt_btn = GUI_obj.widget_items ["pushButton_2"]
        self.fLine      = GUI_obj.widget_items ["textEdit"]
        self.opt = GUI_obj.clicked_comboBox
        self.printUI = GUI_obj.widget_items ["textEdit_2"]


        self.browse_btn.configure ( command = self.getFile)
        self.cvt_btn   .configure ( command = self.convert_btn)
        self.File_name = ''


    def getFile(self):
        file_str = str(filedialog.askopenfilename()) # initialdir = root
        if file_str == '':
            self.fLine.delete('1.0',tk.END)
            #self.fLine.insert(0,text)
            self.File_name = ''
        else:
            self.fLine.delete('1.0',tk.END)
            self.fLine.insert(tk.INSERT, file_str)
            self.File_name = file_str
        print ('file = ' , file_str)

    def convert_btn (self):
        self.printUI.delete('1.0',tk.END)
        gui_lib = self.opt.get()
        if self.File_name  == '':
            pr ('No file selected!')
            return
        fname = self.File_name
        print (gui_lib, fname)
        if gui_lib == "Tkinter":
            cvt_lib = 'tk'
        elif gui_lib == "PyFLTK":
            cvt_lib = 'pyfltk'
        elif gui_lib == "Dear PYGUI":
            cvt_lib = 'dpg'
        elif gui_lib == "IUP C":
            cvt_lib = 'iupcpp'
        elif gui_lib == "iup lua":
            cvt_lib = 'iuplua'
            
        cwd = os.getcwd()
        proc = subprocess.Popen(["python", cwd+"/new_master.py", str(cvt_lib) , fname ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        s1= proc.communicate()[0]
        s2 = s1.decode()
        pr( str( s2))






if __name__ == "__main__":
    app = MainApplication()
    proecss = Processor (app)
    def pr(text):
        #print (text)
        proecss.printUI.insert(tk.INSERT, text+'\n')
    app.show()





