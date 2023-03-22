# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 12:03:14 2023

@author: amrutnp
"""

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
LARGE_FONT= ("Verdana", 12)
class MainApplication():
    def __init__(self):
        self.root = tk.Tk()


        #=========congigure_gui ======================
        self.root.title("MainWindow")
        self.root.geometry("500x500")
        self.root.resizable(True, True)
        ##=========create_widgets ======================
        self.widget_items = {}
        style_obj = ttk.Style()



        self.widget_items ["checkBox"] = ttk.Checkbutton(master = self.root,text='Check box 1',style='checkBox.TCheckbutton');
        self.widget_items ["checkBox"].place(x = 20,y = 150,height=41,width=181,);
        style_obj.configure('checkBox.TCheckbutton', font=('MS Shell Dlg 2', 13)  );


        self.widget_items ["checkBox_4"] = ttk.Checkbutton(master = self.root,text='Check box 2',style='checkBox_4.TCheckbutton',);
        self.widget_items ["checkBox_4"].place(x = 20,y = 130,height=17,width=171,);
        style_obj.configure('checkBox_4.TCheckbutton', font=('MS Shell Dlg 2', 12)  );





    def show(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApplication()
    app.show()





