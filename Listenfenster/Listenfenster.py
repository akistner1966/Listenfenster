# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font as font
import locale as lcl
from random import *
import sqlite3 as sql3

class listenfenster(object):
    def __init__(self, parent, headlne, fields, db_name, srtndx=0, srtdir=True):
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
        self.dbname = db_name
        self.srtndx = srtndx
        self.srtdir = srtdir
        self.fields = fields
        self.bfnt = font.Font(family='Helvetica', weight=font.BOLD)
        self.nfnt = font.Font(family='Helvetica')
        self.top = tk.Toplevel(parent)
        tk.Label(self.top, text=headlne).pack()
        self.frameTop = tk.Frame(self.top) #Rahmen für Kopfzeile
        self.frameTop.pack(side=tk.TOP, fill=tk.BOTH)
        self.frameMid = tk.Frame(self.top) #Rahmen für Inhalt
        self.frameMid.pack(side=tk.TOP, fill=tk.BOTH)
        self.frameDwn = tk.Frame(self.top) #Rahmen für Buttons
        self.frameDwn.pack(side=tk.TOP, fill=tk.BOTH)
        self.txthdln = tk.Text(self.frameTop, height=2, width=150)
        self.txthdln.pack(side=tk.TOP)
        self.txtfeld = tk.Text(self.frameTop, height=40, width=150)
        self.txtfeld.pack(side=tk.TOP)
        self.btnOK = tk.Button(self.frameDwn, text  ='OK', command=self._ok,
                               font=self.nfnt)
        self.btnOK.pack(side=tk.LEFT, padx=5, pady=5)
        self.lbl1 = tk.Label(self.frameDwn, text='     Sortieren nach =>')
        self.lbl1.pack(side=tk.LEFT, padx=5, pady=5)
        self.btnSrtDn = tk.Button(self.frameDwn, text  ='Dateiname',
                                  command=self._srtname, font=self.nfnt)
        self.btnSrtDn.pack(side=tk.LEFT, padx=5, pady=5)
        self.btnSrtXtn = tk.Button(self.frameDwn, text  ='Extension',
                                   command=self._srtextn, font=self.nfnt)
        self.btnSrtXtn.pack(side=tk.LEFT, padx=5, pady=5)
        self.btnSrtGro = tk.Button(self.frameDwn, text  ='Größe',
                                   command=self._srtsize, font=self.nfnt)
        self.btnSrtGro.pack(side=tk.LEFT, padx=5, pady=5)
        self.btnSrtDat = tk.Button(self.frameDwn, text  ='Datum',
                                   command=self._srtdate, font=self.nfnt)
        self.btnSrtDat.pack(side=tk.LEFT, padx=5, pady=5)
        self.lbl2 = tk.Label(self.frameDwn, text='     Sortierrichtung =>')
        self.lbl2.pack(side=tk.LEFT, padx=5, pady=5)
        self.btnSrtUp = tk.Button(self.frameDwn, text  ='Aufsteigend',
                                  command=self._srtup, font=self.nfnt)
        self.btnSrtUp.pack(side=tk.LEFT, padx=5, pady=5)
        self.btnSrtDwn = tk.Button(self.frameDwn, text  ='Absteigend',
                                  command=self._srtdn, font=self.nfnt)
        self.btnSrtDwn.pack(side=tk.LEFT, padx=5, pady=5)
        self._ausgabe()

    def _ausgabe(self):
        mxlen = 5*[0]
        self.txtfeld.delete("1.0","end")
        self.txthdln.delete("1.0","end")
        conn = sql3.connect(self.dbname)
        cursor = conn.execute('SELECT * FROM DATLISTE')
        for row in cursor:
            for cnt, ele in enumerate(row, 0):
                if cnt != 3:
                    mxlen[cnt] = max(mxlen[cnt], len(str(ele)))
                else: #Dateigröße => Tausenderpunkte!
                    mxlen[cnt] = max(mxlen[cnt], len(lcl.format('%d', ele, 1)))
        conn.close()
        mxlen[4] += 2 #Punkte für das Datum berücksichtigen
        for cnt, ele in enumerate(self.fields, 0):
            mxlen[cnt] = max(mxlen[cnt], len(str(ele)))
            self.txthdln.insert(tk.END, ele)
            if cnt < len(self.fields) - 1:
                self.txthdln.insert(tk.END, ' ')
        conn = sql3.connect(self.dbname)
        sqlstr = 'SELECT * FROM DATLISTE ORDER BY '
        if self.srtdir: #Aufsteigend sortieren
            sqldir = ' ASC'
        else: #Absteigend sortieren
            sqldir = ' DESC'
        if self.srtndx == 0: #sortieren nach Dateiname
            cursor = conn.execute(sqlstr + 'NAME' + sqldir)
        if self.srtndx == 1: #sortieren nach Extension dann nach Dateiname
            cursor = conn.execute(sqlstr + 'EXTN, NAME' + sqldir)
        if self.srtndx == 2: #sortieren nach Dateigröße
            cursor = conn.execute(sqlstr + 'SIZE' + sqldir)
        if self.srtndx == 3: #sortieren nach Dateidatum
            cursor = conn.execute(sqlstr + 'FILEDATE' + sqldir)
        for row in cursor:
            for cnt, ele in enumerate(row, 0):
                estr = str(ele)
                if cnt > 0:
                    if cnt == 4: #Datum
                        estr = estr[6:8] + '.' + estr[4:6] + '.' + estr[0:4]
                    elif cnt == 3: #Dateigröße
                        estr = lcl.format('%d', ele, 1)
                        if len(estr) < mxlen[cnt]:
                            elestr = ' '*(mxlen[cnt] - len(estr)) + estr
                        else:
                            elestr = estr
                    if cnt != 3:
                        if len(estr) < mxlen[cnt]:
                            elestr = estr + ' '*(mxlen[cnt] - len(estr))
                        else:
                            elestr = estr
                    self.txtfeld.insert(tk.END, elestr)
                    if cnt < len(row) - 1:
                        self.txtfeld.insert(tk.END, ' ')
            self.txtfeld.insert(tk.END, '\n')
        conn.close()
        self._btnconfig()

    def _srtname(self):
        self.srtndx = 0 #sortieren nach Dateiname
        self._ausgabe()

    def _srtextn(self):
        self.srtndx = 1 #sortieren nach Extension und dann nach Dateiname
        self._ausgabe()

    def _srtsize(self): #sortieren nach Dateigröße
        self.srtndx = 2
        self._ausgabe()

    def _srtdate(self):
        self.srtndx = 3 #sortieren nach Dateidatum
        self._ausgabe()

    def _srtup(self):
        self.srtdir = True
        self._ausgabe()

    def _srtdn(self):
        self.srtdir = False
        self._ausgabe()

    def _cuttrim(self, ein, ndx, mxlen):
        if ndx != 2: #linksbündig
            if len(ein) < mxlen:
                ein += (mxlen - len(ein))*' '
        else: #rechtsbündig
            if len(ein) < mxlen:
                ein = (mxlen - len(ein))*' ' + ein
        return(ein)

    def _ok(self):
        self.top.destroy()

    def _btnconfig(self):
        self.btnSrtDn.config(font=self.nfnt)
        self.btnSrtXtn.config(font=self.nfnt)
        self.btnSrtGro.config(font=self.nfnt)
        self.btnSrtDat.config(font=self.nfnt)
        self.btnSrtUp.config(font=self.nfnt)
        self.btnSrtDwn.config(font=self.nfnt)
        if self.srtndx == 0: #sortieren nach Dateiname
            self.btnSrtDn.config(font=self.bfnt)
        elif self.srtndx == 1: #sortieren nach Extension dann nach Dateiname
            self.btnSrtXtn.config(font=self.bfnt)
        elif self.srtndx == 2: #sortieren nach Dateigröße
            self.btnSrtGro.config(font=self.bfnt)
        elif self.srtndx == 3: #sortieren nach Dateidatum
            self.btnSrtDat.config(font=self.bfnt)
        if self.srtdir: #aufsteigend sortieren
            self.btnSrtUp.config(font=self.bfnt)
        else: #absteigend sortieren
            self.btnSrtDwn.config(font=self.bfnt)

def mkstr(einlst):
    einlst[2] = locale.format('%d', einlst[2], 1)
    return(einlst)

def vornull(ein):
    if ein >= 10:
        return(str(ein))
    else:
        return('0' + str(ein))

def mklst():
    conn = sql3.connect(dbname)
    droptable = 'DROP TABLE DATLISTE'
    try:
        conn.execute(droptable)
    except:
        pass
    conn.close()
    conn = sql3.connect(dbname)
    sqlcmd = 'CREATE TABLE IF NOT EXISTS DATLISTE (\
    ID INTEGER PRIMARY KEY, NAME TEXT NOT NULL, \
    EXTN TEXT NOT NULL, SIZE INTEGER NOT NULL, \
    FILEDATE INTEGER NOT NULL);'
    conn.execute(sqlcmd)
    dlst = []
    xtnlst = ['doc', 'xls', 'ppt', 'txt', 'bat', 'jpg', 'png', 'cdr']
    bcnt = 65 #ASCII-Code für 'A'
    zcnt = 48 #ASCII-Code für '0'
    for i in range(100):
        dmo = randint(1, 12)
        if dmo == 2:
            dta = randint(1, 28)
        elif dmo in [1, 3, 5, 7, 8, 10, 12]:
            dta = randint(1, 31)
        else:
            dta = randint(1, 30)
        dja = 2000 + randint(0, 19)
        datstr = str(dja) + vornull(dta) + vornull(dmo)
        dgr = randint(1, 100000)
        xtnptr = randint(0, 7)
        dname = chr(bcnt) + chr(zcnt) + '.' + xtnlst[xtnptr]
        zcnt += 1
        if zcnt > 57:
            zcnt = 48
            bcnt +=1
        insstr = 'INSERT INTO DATLISTE (ID,NAME,EXTN,SIZE,FILEDATE)'
        insstr += 'VALUES(' + str(i) + ','
        insstr += quote(dname) + ',' + quote(xtnlst[xtnptr])
        insstr += ',' + str(dgr) + ',' + datstr + ');'
        conn.execute(insstr)
    conn.commit()
    conn.close()

def mkfields():
    return(['Dateiname', 'Extension', 'Dateigröße', 'Dateidatum'])

def showlist():
    lf = listenfenster(root, 'Demoliste', fliste, dbname, 2, False)

def quote(ein):
    return('"' + ein + '"')

if __name__== "__main__":
    lcl.setlocale(lcl.LC_NUMERIC, '')
    dbname = 'verzeichnis.db' #Datenbank wird im Arbeitsspeicher abgebildet
    root = tk.Tk()
    fliste = mkfields()
    mklst()
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Datei', underline=0, menu = filemenu)
    filemenu.add_command(label='Liste anzeigen', underline=0,
                         command=showlist, accelerator='')
    filemenu.add_command(label='Beenden', underline=0,
                         command=root.destroy, accelerator='Alt+F4')
    root.config(menu = menubar)
    root.mainloop()