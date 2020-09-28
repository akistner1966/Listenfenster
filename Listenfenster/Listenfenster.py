# -*- coding: utf-8 -*-

import tkinter as tk

class listenfenster(object):
    def __init__(self, parent, headlne, fields, content):
        self.top = tk.Toplevel(parent)
        tk.Label(self.top, text=headlne).pack()
        self.frameTop = tk.Frame(self.top) #Rahmen für Kopfzeile
        self.frameTop.pack(side=tk.TOP, fill=tk.BOTH)
        self.frameMid = tk.Frame(self.top) #Rahmen für Inhalt
        self.frameMid.pack(side=tk.TOP, fill=tk.BOTH)
        self.frameDwn = tk.Frame(self.top) #Rahmen für Buttons
        self.frameDwn.pack(side=tk.TOP, fill=tk.BOTH)
        self.txthdln = tk.Text(self.frameTop, height=5, width=150)
        self.txthdln.pack(side=tk.TOP)
        self.txtfeld = tk.Text(self.frameTop, height=40, width=150)
        self.txtfeld.pack(side=tk.TOP)
        self.btnOK = tk.Button(self.frameDwn, text  ='OK', command=self.ok)
        self.btnOK.pack(side=tk.LEFT, padx=5, pady=5)
        for datensatz in content: #Textfeld füllen
            for ele in datensatz:
                self.txtfeld.insert(tk.END, ele)
            self.txtfeld.insert(tk.END, '\n')
        
    def ok(self):
        self.top.destroy()

def mklst():
    dlst = []
    ele = ['A.xls', 'xls', 260, '01.12.2001']
    dlst.append(ele)
    ele = ['B.xls', 'xls', 1350, '01.12.2004']
    dlst.append(ele)
    ele = ['C.xls', 'xls', 12260, '01.11.2001']
    dlst.append(ele)
    ele = ['A.txt', 'txt', 260, '11.12.2011']
    dlst.append(ele)
    ele = ['B.txt', 'txt', 1350, '10.12.2014']
    dlst.append(ele)
    ele = ['C.txt', 'txt', 12260, '01.08.2011']
    dlst.append(ele)
    ele = ['A.jpg', 'jpg', 260, '01.01.2011']
    dlst.append(ele)
    ele = ['B.jpg', 'jpg', 1350, '01.07.2007']
    dlst.append(ele)
    ele = ['C.jpg', 'jpg', 12260, '01.04.2016']
    dlst.append(ele)
    ele = ['A.png', 'png', 260, '15.12.2011']
    dlst.append(ele)
    ele = ['B.png', 'png', 1350, '18.12.2014']
    dlst.append(ele)
    ele = ['C.png', 'png', 12260, '04.08.2011']
    dlst.append(ele)
    ele = ['A.doc', 'doc', 260, '12.03.2020']
    dlst.append(ele)
    ele = ['B.doc', 'doc', 21350, '18.08.2019']
    dlst.append(ele)
    ele = ['C.doc', 'doc', 212260, '08.04.2010']
    dlst.append(ele)
    return(dlst)

def mkfields():
    return(['Dateiname', 'Extension', 'Dateigröße', 'Dateindatum'])

def showlist():
    lf = listenfenster(root, 'Demoliste', fliste, dliste)

if __name__== "__main__":
    root = tk.Tk()
    dliste = mklst()
    fliste = mkfields()
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Datei', underline=0, menu = filemenu)
    filemenu.add_command(label='Liste anzeigen', underline=0,
                         command=showlist, accelerator='')
    filemenu.add_command(label='Beenden', underline=0,
                         command=root.destroy, accelerator='Alt+F4')
    root.config(menu = menubar)
    root.mainloop()