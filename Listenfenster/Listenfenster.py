# -*- coding: utf-8 -*-

import tkinter as tk
import locale

class listenfenster(object):
    def __init__(self, parent, headlne, fields, content, srtndx=0, srtdir=True):
        """
        mit <strndx> wird das Feldes angegeben, nach dem sortiert
        werden soll. Es gilt:
        <srtndx> = 0 - sortieren nach Dateiname
        <srtndx> = 1 - sortieren nach Extension und dann nach Dateiname
        <srtndx> = 2 - sortieren nach Dateigröße
        <srtndx> = 3 - sortieren nach Dateidatum
        <strdir> = True: Es wird aufsteigend sortiert
        <strdir> = False: Es wird absteigend sortiert
        """
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
        sortiert = False
        while not sortiert:
            sortiert = True
            for cnt, dsatz in enumerate(content, 0):
                if srtndx == 0: #sortieren nach Dateiname
                    if cnt < len(content) - 1:
                        dsnext = content[cnt + 1]
                        if srtdir: #aufsteigend sortieren
                            if dsatz[0] > dsnext[0]:
                                sortiert = False
                                dmy = content[cnt + 1]
                                content[cnt + 1] = content[cnt]
                                content[cnt] = dmy
                        else: #absteigend sortieren
                            if dsatz[0] < dsnext[0]:
                                sortiert = False
                                dmy = content[cnt + 1]
                                content[cnt + 1] = content[cnt]
                                content[cnt] = dmy
                elif srtndx == 1: #sortieren nach Extension, dann Dateiname
                    if cnt < len(content) - 1:
                        dsnext = content[cnt + 1]
                        dnxtnxt = dsnext[1] + ' ' + dsnext[0]
                        dnxtact = dsatz[1] + ' ' + dsatz[0]
                        if srtdir: #aufsteigend sortieren
                            if dnxtact > dnxtnxt:
                                sortiert = False
                                dmy = content[cnt + 1]
                                content[cnt + 1] = content[cnt]
                                content[cnt] = dmy
                        else: #absteigend sortieren
                            if dnxtact < dnxtnxt:
                                sortiert = False
                                dmy = content[cnt + 1]
                                content[cnt + 1] = content[cnt]
                                content[cnt] = dmy
                elif srtndx == 2: #sortieren nach Dateigröße
                    if cnt < len(content) - 1:
                        inplst = content[cnt + 1]
                        grnxt = int(inplst[2].replace('.', ''))
                        inplst = content[cnt]
                        gract = int(inplst[2].replace('.', ''))
                        if srtdir: #aufsteigend sortieren
                            if gract > grnxt:
                                sortiert = False
                                dmy = content[cnt + 1]
                                content[cnt + 1] = content[cnt]
                                content[cnt] = dmy
                        else: #absteigend sortieren
                            if gract < grnxt:
                                sortiert = False
                                dmy = content[cnt + 1]
                                content[cnt + 1] = content[cnt]
                                content[cnt] = dmy
                elif srtndx == 3: #sortieren nach Datum
                    if cnt < len(content) - 1:
                        inplst = content[cnt + 1]
                        datlst = inplst[3].split('.')
                        dtnxt = int(10000*datlst[2]) + 100*int(datlst[1]) + \
                            int(datlst[0])
                        inplst = content[cnt]
                        datlst = inplst[3].split('.')
                        dtact = int(10000*datlst[2]) + 100*int(datlst[1]) + \
                            int(datlst[0])
                        if srtdir: #aufsteigend sortieren
                            if dtact > dtnxt:
                                sortiert = False
                                dmy = content[cnt + 1]
                                content[cnt + 1] = content[cnt]
                                content[cnt] = dmy
                        else: #absteigend sortieren
                            if dtact < dtnxt:
                                sortiert = False
                                dmy = content[cnt + 1]
                                content[cnt + 1] = content[cnt]
                                content[cnt] = dmy
        mxlen = [0]*4
        for dsatz in content: #Max-Längen ermitteln - Teil 1
            for cnt, ele in enumerate(dsatz, 0):
                mxlen[cnt] = max(mxlen[cnt], len(ele))
        for cnt, ele in enumerate(fields, 0): #Max-Längen ermitteln - Teil 2
            mxlen[cnt] = max(mxlen[cnt], len(ele))
        for cnt, ele in enumerate(fields, 0):
            self.txthdln.insert(tk.END, ele)
            if cnt < len(fields) - 1:
                self.txthdln.insert(tk.END, ' ')
        for dsatz in content: #Textfeld füllen
            for cnt, ele in enumerate(dsatz, 0):
                self.txtfeld.insert(tk.END,
                                    self._cuttrim(ele, cnt, mxlen[cnt]))
                if cnt < len(dsatz) - 1:
                    self.txtfeld.insert(tk.END, ' ')
                else:
                    self.txtfeld.insert(tk.END, '\n')

    def _cuttrim(self, ein, ndx, mxlen):
        if ndx != 2: #linksbündig
            if len(ein) < mxlen:
                ein += (mxlen - len(ein))*' '
        else: #rechtsbündig
            if len(ein) < mxlen:
                ein = (mxlen - len(ein))*' ' + ein
        return(ein)

    def ok(self):
        self.top.destroy()

def mkstr(einlst):
    einlst[2] = locale.format('%d', einlst[2], 1)
    return(einlst)

def mklst():
    dlst = []
    ele = ['A.xls', 'xls', 260, '01.12.2001']
    dlst.append(mkstr(ele))
    ele = ['B.xls', 'xls', 1350, '01.12.2004']
    dlst.append(mkstr(ele))
    ele = ['C.xls', 'xls', 12260, '01.11.2001']
    dlst.append(mkstr(ele))
    ele = ['A.txt', 'txt', 260, '11.12.2011']
    dlst.append(mkstr(ele))
    ele = ['B.txt', 'txt', 1350, '10.12.2014']
    dlst.append(mkstr(ele))
    ele = ['C.txt', 'txt', 12260, '01.08.2011']
    dlst.append(mkstr(ele))
    ele = ['A.jpg', 'jpg', 260, '01.01.2011']
    dlst.append(mkstr(ele))
    ele = ['B.jpg', 'jpg', 1350, '01.07.2007']
    dlst.append(mkstr(ele))
    ele = ['C.jpg', 'jpg', 12260, '01.04.2016']
    dlst.append(mkstr(ele))
    ele = ['A.png', 'png', 260, '15.12.2011']
    dlst.append(mkstr(ele))
    ele = ['B.png', 'png', 1350, '18.12.2014']
    dlst.append(mkstr(ele))
    ele = ['C.png', 'png', 12260, '04.08.2011']
    dlst.append(mkstr(ele))
    ele = ['A.doc', 'doc', 260, '12.03.2020']
    dlst.append(mkstr(ele))
    ele = ['B.doc', 'doc', 21350, '18.08.2019']
    dlst.append(mkstr(ele))
    ele = ['C.doc', 'doc', 212260, '08.04.2010']
    dlst.append(mkstr(ele))
    return(dlst)

def mkfields():
    return(['Dateiname', 'Extension', 'Dateigröße', 'Dateidatum'])

def showlist():
    lf = listenfenster(root, 'Demoliste', fliste, dliste, 3, True)

if __name__== "__main__":
    locale.setlocale(locale.LC_NUMERIC, '')
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