############################################################
# main.py
############################################################

from random import choices
from turtle import onclick
import wx
import datetime
import wx.adv
import requests

from uiGlobal import * 
# import uiGlobal
import os
import sys

import json
import time
from aboutDialog import *
import login
from requests.structures import CaseInsensitiveDict
import csv
import webbrowser
import shelve
from pathlib import Path

import sqlite3
from sqlite3 import Error

class MultiStatus (wx.StatusBar):
   
    def __init__ (self, parent):
       
        wx.StatusBar.__init__(self, parent, -1)
        # Sets the number of field count "5"
        self.SetFieldsCount(3)
        # Sets the widths of the fields in the status bar.
        #self.SetStatusWidths([-1, -1, -3, -2, -10])
        self.SetStatusWidths([-4, -2, -3])

class TestPanel(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self,None, size=(530,620))

        self.SetBackgroundColour("White")
        self.SetTitle('MCCI Brix UI')

        self.listview = []
        self.token = None

        self.conn = None

        self.user = "unknown"
        self.location = "Arnot"
        self.brixVal = "1.0"
        self.btime = None
        self.bdate = None

        self.vboxParent = wx.BoxSizer(wx.VERTICAL)
        #self.hboxdr1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxdr2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxdr3 = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxdr4 = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxdr5 = wx.BoxSizer(wx.HORIZONTAL)

        self.hboxdr6 = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxdr7 = wx.BoxSizer(wx.HORIZONTAL)
        
        ab = wx.StaticBox(self, -1, "Manual Entry Form", size = (400, 200))
        self.vboxData = wx.StaticBoxSizer(ab, wx.VERTICAL)
        bc = wx.StaticBox(self, -1, "View Last Data", size = (400, 200))
        self.vboxRead = wx.StaticBoxSizer(bc, wx.HORIZONTAL)
        ca = wx.StaticBox(self, -1, "Logwindow", size = (400, 200))
        self.vboxLog = wx.StaticBoxSizer(ca, wx.HORIZONTAL)


        #self.stxt_title = wx.StaticText(self, -1, "Sap Sugar (Brix) Manual Entry Form", size = (-1, -1))

        # self.ihboxdr1 = wx.BoxSizer(wx.HORIZONTAL)
        # self.ihboxdr1.Add(self.stxt_title, flag=wx.LEFT , border=0)
        # self.hboxdr1.Add(self.ihboxdr1 ,flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border= 100)

        
        self.st_loc = wx.StaticText(self, -1, "Location ", size = (60, 15))
        self.cb_list = ["Arnot", "Uihlein", "UVM"]
        self.brix_loc = wx.ComboBox(self, -1, choices = self.cb_list, size = (75, 25))
    
        self.ihboxdr2 = wx.BoxSizer(wx.HORIZONTAL)
        self.ihboxdr2.Add(self.st_loc, flag=wx.LEFT , border=0)
        self.ihboxdr2.Add(self.brix_loc, flag=wx.LEFT, border = 45)

        self.hboxdr2.Add(self.ihboxdr2, flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border= 10)
        self.hboxdr2.Add(0,1,0)
        self.st_brix = wx.StaticText(self, -1, "Brix in% ", size = (60, 15))
        
        self.tc_brix = wx.TextCtrl(self, -1, "3.0" , style = wx.TE_PROCESS_ENTER,
                                    size = (65, 25),validator=NumericValidator())

        self.ihboxdr3 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.ihboxdr3.Add(self.st_brix, flag=wx.LEFT, border=10)
        self.ihboxdr3.Add(self.tc_brix, flag=wx.LEFT, border = 45)
        #self.ihboxdr3.Add(self.tc_UiHlein, flag=wx.LEFT, border = 20)
        #self.ihboxdr3.Add(self.tc_UVM, flag=wx.LEFT, border = 20)
        self.hboxdr3.Add(self.ihboxdr3, flag=wx.ALIGN_CENTER_VERTICAL)

        
        self.ihboxdr4 = wx.BoxSizer(wx.HORIZONTAL)
        self.st_tm = wx.StaticText(self, -1, "DateTime", size = (60, 15))
        self.tp = wx.adv.TimePickerCtrl(self,size=(120,-1) )
        self.dp = wx.adv.DatePickerCtrl(self, size=(120,-1),
                                       style = wx.TAB_TRAVERSAL
                                       | wx.adv.DP_DROPDOWN
                                       | wx.adv.DP_SHOWCENTURY
                                       | wx.adv.DP_ALLOWNONE )

        self.ihboxdr4.Add(self.st_tm, flag=wx.LEFT, border = 10)
        self.ihboxdr4.Add(self.tp, flag=wx.LEFT, border = 45)
        self.ihboxdr4.Add(self.dp, flag=wx.LEFT, border = 0)
        self.hboxdr4.Add(self.ihboxdr4, flag = wx.LEFT, border = 0)

        self.ihboxdr5 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_Submit = wx.Button(self, -1, "Submit", size = (65, 25))
        self.ihboxdr5.Add(self.btn_Submit, flag=wx.LEFT, border = 180)
        self.hboxdr5.Add(self.ihboxdr5, flag=wx.ALIGN_CENTER_VERTICAL )
        #self.btn_Submit.Disable()

        self.ihboxdr6 = wx.BoxSizer(wx.HORIZONTAL)
        self.viewdata = wx.StaticText(self, -1, "View", size = (-1, -1))
        self.btn_v10 = wx.Button(self, -1, "Last 10", size = (63, 25))
        self.btn_v30 = wx.Button(self, -1, "Last 30", size = (63, 25))
        self.btn_vall = wx.Button(self, -1, "All", size = (63, 25))
        self.btn_clear = wx.Button(self, -1, "Clear", size = (63, 25))
        self.btn_save = wx.Button(self, -1, "CSV Download", size = (90,25))

        self.ihboxdr6.Add(self.viewdata, flag=wx.LEFT | 
                        wx.ALIGN_CENTER_VERTICAL, border=10)
        self.ihboxdr6.Add(self.btn_v10, flag=wx.LEFT, border=10)

        self.ihboxdr6.Add(self.btn_v30, flag=wx.LEFT, border = 25)

        self.ihboxdr6.Add(self.btn_vall, flag=wx.LEFT, border = 25)
        self.ihboxdr6.Add(self.btn_clear, flag=wx.LEFT, border = 25)
        self.ihboxdr6.Add(self.btn_save, flag=wx.LEFT, border = 13)

        self.hboxdr6.Add(self.ihboxdr6, flag=wx.ALIGN_CENTER_VERTICAL)

        self.ihboxdr7 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.Logwindow = wx.TextCtrl(self, 0, "", style = wx.TE_MULTILINE|wx.TE_READONLY,
                                     size = (470, 300))
        self.hboxdr7.Add(self.Logwindow, flag=wx.LEFT | 
                        wx.ALIGN_CENTER_VERTICAL, border=10)
                        
        self.tc_brix.SetMaxLength(3)
        
        now = datetime.date.today()
        self.ndate = now

        self.vboxData.AddMany([
            # (self.hboxdr1, 1, wx.EXPAND | wx.ALL, 5),
            (self.hboxdr2, 1, wx.EXPAND | wx.ALL, 5),
            (self.hboxdr3,1,wx.EXPAND | wx.ALL, 5),
            (self.hboxdr4,1,wx.EXPAND | wx.ALL, 5),
            (self.hboxdr5,1,wx.EXPAND | wx.ALL, 5)
        ])

        self.vboxRead.AddMany([
            (0,10,0),
            (self.hboxdr6, 1, wx.EXPAND | wx.ALL, 5),
            (0,15,0)
        ])

        self.vboxLog.AddMany([
            (self.hboxdr7, 1, wx.EXPAND | wx.ALL)
        ])

        self.vboxParent.AddMany([
            (self.vboxData, 0, wx.EXPAND | wx.ALL, 10),
            (self.vboxRead, 0, wx.EXPAND | wx.ALL, 10),
            (self.vboxLog, 0, wx.EXPAND | wx.ALL, 10)
        ])

        self.SetSizer(self.vboxParent)

        base = os.path.abspath(os.path.dirname(__file__))
        self.SetIcon(wx.Icon(base+"/icons/"+IMG_LOGO))
        self.Centre()
        self.Show()

        self.btn_Submit.Bind(wx.EVT_BUTTON, self.StartSubmit)
        self.tc_brix.Bind(wx.EVT_TEXT_MAXLEN, self.OnEnterArnot)
        self.brix_loc.Bind(wx.EVT_COMBOBOX, self.OnCombox)
        self.btn_v10.Bind(wx.EVT_BUTTON, self.onEnterten)
        self.btn_v30.Bind(wx.EVT_BUTTON, self.onEnterthirty)
        self.btn_vall.Bind(wx.EVT_BUTTON, self.onEnterninty)
        self.btn_clear.Bind(wx.EVT_BUTTON, self.onEnterclear)
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.Bind(wx.EVT_MENU, self.MenuHandler)
        self.Bind(wx.EVT_MENU, self.OnClickHelp, id=ID_MENU_HELP_WEB)
        self.Bind(wx.EVT_MENU, self.OnClickHelp, id=ID_MENU_HELP_PORT)
        self.Bind(wx.EVT_MENU, self.OnClickHelp, id=ID_MENU_HELP_PDB)
        self.Bind(wx.EVT_MENU, self.OnClickHelp, id=ID_MENU_HELP_DNC)
        self.btn_save.Bind(wx.EVT_BUTTON, self.OnSave)
        self.Bind(wx.EVT_CLOSE, self.FrameClose)
        
        fileMenu = wx.Menu()
        fileMenu.Append(ID_MENU_FILE_CLOSE, "&Close \tAlt+F4")

        helpMenu = wx.Menu()
        helpMenu.AppendSeparator()
        helpMenu.Append(ID_MENU_HELP_WEB, "MCCI Website")
        helpMenu.Append(ID_MENU_HELP_PORT, "MCCI Support Portal")
        helpMenu.AppendSeparator()
        helpMenu.Append(ID_MENU_HELP_PDB, "Public Dashboard")
        helpMenu.Append(ID_MENU_HELP_DNC, "DNC Server")
        helpMenu.AppendSeparator()
        helpMenu.Append(ID_MENU_HELP_ABOUT, "About...")

        loginMenu = wx.Menu()
        loginMenu.Append(ID_MENU_LOGIN, "Login")
        # create menubar
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu,    "&File")
        menuBar.Append(loginMenu,    "&User Login")
        menuBar.Append(helpMenu,    "&Help")

        self.SetMenuBar(menuBar)
        self.statusbar = MultiStatus(self)
        self.SetStatusBar(self.statusbar)

        self.brix_loc.SetValue("Arnot")

        self.connect_db()
        self.create_table()
        self.read_db_data()
        self.brix_loc.SetValue(self.location)
        self.tc_brix.SetValue(self.brixVal)
            
    def FrameClose(self, evt):
        self.preserve_data()
        evt.Skip()

    def preserve_data(self):
        loc = self.brix_loc.GetValue()
        brix = self.tc_brix.GetValue()
        
        dt = self.dp.GetValue()
        tm = self.tp.GetValue()
        strtm = tm.Format("%H:%M:%S")
        
        strdt = ""
        try:
            strdt = dt.Format("%m-%d-%Y")
        except:
            strdt = datetime.date.today()
        dlist = []
        dlist.append(loc)
        dlist.append(brix)
        dlist.append(strtm)
        dlist.append(strdt)
        self.LoadDataToDB(dlist)

    
         
    def OnClickHelp(self, event):
        id = event.GetId()   
        if(id == ID_MENU_HELP_WEB):
            webbrowser.open(mcci_web, new=0, autoraise=True)
        elif(id == ID_MENU_HELP_PORT):
            webbrowser.open(mcci_support, new=0,
                            autoraise=True)
        elif(id == ID_MENU_HELP_PDB):
            webbrowser.open(brixui_dashboard,
                            new = 0, autoraise=True)
        elif(id == ID_MENU_HELP_DNC):
            webbrowser.open(dncui,
                            new = 0, autoraise=True)

    def OnCombox(self, event):
        self.Logwindow.Clear()
        self.location = self.brix_loc.GetValue()
        self.Logwindow.write("selected Location is  " + self.location + "\n")
        self.SetStatusText("Location " + self.location)
        
    def StartSubmit(self, evt):
        if self.token == None:
            self.SetStatusText("Please Login to server")
            wx.MessageBox("Please Login to Server", "Warning Message",  wx.OK | wx.ICON_WARNING)
            return
        
        url = root_Url + "brix"
        loc = self.location
        brix = self.tc_brix.GetValue()
        
        dt = self.dp.GetValue()
        tm = self.tp.GetValue()
        strtm = tm.Format("%H:%M:%S")
        strdt = ""
        try:
            strdt = dt.Format("%m-%d-%Y")
        except:
            strdt = datetime.date.today()
        strdate = strdt+","+strtm

        payload = { loc: brix,"rdate":strdate}

        headers = {'Authorization' : 'Bearer ' + self.token}
        resp = requests.post(url, headers=headers, data = payload)
        if(resp.status_code == 502):
            self.Logwindow.write("\nServer unreachable")
        elif(resp.status_code == 400):
            D=json.loads(resp.text)
            wx.MessageBox(D['message'] , "Alert Message",  wx.OK | wx.ICON_WARNING)
        else:
            self.Logwindow.Clear()
            time.sleep(0.1)
            jsresp = resp.json()
            msg = jsresp["message"]
            substr = "Data already exists"
            self.Logwindow.write("\n"+msg)
            if(substr in msg):
                dlgtitle = "Data update alert"
                dlgmsg = "Brix Data already in record, do you want to update once ?"
                dlg = wx.MessageDialog(self, dlgmsg , dlgtitle,  wx.NO | wx.YES)
                if(dlg.ShowModal() == wx.ID_YES):
                    resp = requests.put(url, headers=headers, data = payload)
                    jsresp = resp.json()
                    msg = jsresp["message"]
                    self.Logwindow.write("\n"+msg)
                else:
                    print("No I don't want to update")

    def LoadDataToDB(self, dlist):
        self.connect_db()
        self.create_table()
        self.update_data(dlist)

    def connect_db(self):
        self.conn = None
        try:
            lpath = self.get_user_data_dir()
            dpath = os.path.join(lpath, "MCCI", "Brix")

            os.makedirs(dpath, exist_ok=True)
            fpath = os.path.join(dpath, "brix.db")
            self.conn = sqlite3.connect(fpath)
            return self.conn
        except Error as er:
            print(er)

    def create_table(self):
        sql_tbl = """CREATE TABLE IF NOT EXISTS bdata (id integer PRIMARY KEY,
                      loc text, brixval text, btime text, bdate text, buser text);"""
        try:
            c = self.conn.cursor()
            c.execute(sql_tbl)
        except Error as er:
            print(er)

    def read_db_data(self):
        sql_read_qry = """SELECT * from bdata"""
        try:
            c= self.conn.cursor()
            c.execute(sql_read_qry)
            rec = c.fetchall()
            if(len(rec) > 0):
                #print(rec[0][0], rec[0][1], rec[0][2], rec[0][3], rec[0][4], rec[0][5])
                self.location = rec[0][1]
                self.brixVal = rec[0][2]
                self.btime = rec[0][3]
                self.bdate = rec[0][4]
                self.user = rec[0][5]
            else:
                print("No data found")
        except Error as er:
            print(er)

    def update_data(self, dlist):
        sql_read_qry = """SELECT * from bdata"""
        try:
            c= self.conn.cursor()
            c.execute(sql_read_qry)
            rec = c.fetchall()
            if(len(rec) == 0):
                self.insert_data(dlist)
            else:
                self.update_bdata(dlist)
        except Error as er:
            print(er)

    def insert_data(self, dlist):
        sql_qry = """INSERT INTO bdata (loc, brixval, btime, bdate, buser) VALUES (?,?,?,?,?)"""

        try:
            c= self.conn.cursor()
            c.execute(sql_qry,(dlist[0],
                      dlist[1], dlist[2], dlist[3], self.user))
            self.conn.commit()
            print("Data insert success: ", c.rowcount)
        except Error as er:
            print(er)
        
    
    def update_bdata(self, dlist):
        sql_qry = """UPDATE bdata SET loc = ?, brixval = ?, btime = ?, bdate = ?, buser = ? WHERE id = 1"""

        try:
            c= self.conn.cursor()
            c.execute(sql_qry,(dlist[0],
                      dlist[1], dlist[2], dlist[3], self.user))
            self.conn.commit()
            print("Data update success: ", c.rowcount)
        except Error as er:
            print(er)

    def update_buser(self):
        sql_qry = """UPDATE bdata SET buser = ? WHERE id = 1"""

        try:
            c= self.conn.cursor()
            c.execute(sql_qry, [self.user])
            self.conn.commit()
        except Error as er:
            print(er)

    def onEnterten(self, evt):
        self.SetStatusText("View Last Ten data")
        
        if self.token == None:
            self.SetStatusText("Please Login to server")
            wx.MessageBox("Please Login to Server", "Warning Message",  wx.OK | wx.ICON_WARNING)
            return
        else:
            self.SetStatusText("View Last Ten")
        url = root_Url + "brix/"+self.location
        
        headers = {'Authorization' : 'Bearer ' + self.token}
        resp = requests.get(url, headers=headers)
        sapdata = resp.json()
        actualen = len(sapdata)
        reqlen = 10
        if actualen < reqlen:
           reqlen = actualen
        for i in range(reqlen):
           self.Logwindow.write("\n"+ sapdata[i]["rdate"].split("T")[0] + ",  "+   self.location +" : "+ sapdata[i][self.location] + "\n")

    def onEnterthirty(self, evt):
        
        self.Logwindow.Clear()
        #self.SetStatusText("View Last Thirt data")
        
        if self.token == None:
            self.SetStatusText("Please Login to server")
            wx.MessageBox("Please Login to Server", "Warning Message",  wx.OK | wx.ICON_WARNING)
            return
        else:
            self.SetStatusText("View Last Thirty data")
   
        url = root_Url + "brix/"+self.location
        
        headers = {'Authorization' : 'Bearer ' + self.token}
        resp = requests.get(url, headers=headers)
        sapdata = resp.json()
        actualen = len(sapdata)
        reqlen = 30
        if actualen < reqlen:
           reqlen = actualen
        for i in range(reqlen):
           self.Logwindow.write(sapdata[i]["rdate"].split("T")[0] + ",  "+   self.location +" : "+ sapdata[i][self.location] + "\n")
    
    def onEnterninty(self, evt):
        self.SetStatusText("View All Data")
        self.Logwindow.Clear()
        if self.token == None:
            self.SetStatusText("Please Login to server")
            wx.MessageBox("Please Login to Server", "Warning Message",  wx.OK | wx.ICON_WARNING)
            return
        else:
            self.SetStatusText("View All data")
   
        url = root_Url + "brix/"+self.location
        headers = {'Authorization' : 'Bearer ' + self.token}
        resp = requests.get(url, headers=headers)
        sapdata = resp.json()
        for i in range(len(sapdata)):
            self.Logwindow.write(sapdata[i]["rdate"].split("T")[0] + ",  "+   self.location +" : "+ sapdata[i][self.location] + "\n")
           
    def onEnterclear(self, evt):
        self.SetStatusText("Clear Logwindow")
        self.Logwindow.Clear()
           
    def OnDateChanged(self, evt):
    
        sel_date = evt.GetDate()
        print (sel_date.Format("%Y-%m-%d"))
        self.set_date(sel_date)
    
    def OnTimeChanged(self, evt):
        return print("%s:%s:%ssec\n" % self.dpc1.GetTime())

    def set_date(self, ndate):
        self.ndate = ndate

    def get_date(self):
        return self.ndate

    def OnEnterArnot(self, event):
        arnot = self.tc_brix.GetValue()
        if(arnot == ""):
            arnot = "1.0"
        pval = float(arnot)
        if(pval > 3.0):
            pval = 1.0
        else:
            pass
            
        self.tc_brix.SetValue(str(pval))
        return self.tc_brix.GetValue()
    
    def MenuHandler(self, e):
        id = e.GetId()
        if(id == ID_MENU_FILE_CLOSE):
            self.OnCloseWindow()
        elif(id == ID_MENU_HELP_ABOUT):
            self.OnAboutWindow()
        elif(id == ID_MENU_LOGIN):
            self.OnLoginWindow()

    def set_UVM(self, strval):
        self.tc_UVM.SetValue(strval)
    
    def get_Arnot(self):
        self.text_Arnot = self.tc_brix.GetValue()
        self.tc_brix.SetValue(self.text_Arnot)
        
        return self.tc_brix.GetValue()

    def get_all_three(self):
        self.ar = float(self.get_Arnot())
       
    def OnAboutWindow(self):
        dlg = AboutDialog(self, self)
        dlg.ShowModal()
        dlg.Destroy()

    def OnLoginWindow(self):
        self.dlg = login.LogIn(self, self)
        self.dlg.Show()
    
    def OnSave(self, evt):
        url = root_Url + "brix/"+self.location
        headers = {'Authorization' : 'Bearer ' + self.token}
        resp = requests.get(url, headers=headers)
        sapdata = resp.json()
        actualen = len(sapdata)
        datearr = []
        dataarr = []
        for i in range(actualen):
            datearr.append(sapdata[i]["rdate"])
            dataarr.append(sapdata[i][self.location])
       
        self.save_file(datearr, dataarr)

    
    def save_file(self, datearr, dataarr):
        self.dirname = ""
        dlg = wx.FileDialog(self, "Save as", self.dirname, "", "*.csv", 
                            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        
        if dlg.ShowModal() == wx.ID_OK:
            wx.BeginBusyCursor()
            dirname = dlg.GetDirectory()
            filename = os.path.join(dirname, dlg.GetFilename())
            if (os.path.isdir(dirname) and os.access(dirname, os.X_OK | 
                                                    os.W_OK)):
                self.dirname = dirname
                rows = zip(datearr, dataarr)
                with open(filename, 'w', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    fields = ['DateTime', self.location]
                    csvwriter.writerow(fields)
                    for row in rows:
                        csvwriter.writerow(row)
            dlg.Destroy()

        if (wx.IsBusy()):
            wx.EndBusyCursor()
        return
    
    def OnCloseWindow (self):
        # Close this window
        self.preserve_data()
        self.Close(True)
    
    def get_user_data_dir(self):
        
        if sys.platform == "win32":
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
            dir_,_ = winreg.QueryValueEx(key, "Local AppData")
            dpath = Path(dir_).resolve(strict=False)
        elif sys.platform == "darwin":
            dpath = Path('~/Library/Application Support/').expanduser()
        else:
            dpath = Path(getenv('XDG_DATA_HOME', "~/.local/lib")).expanduser()
        return dpath

    def OnChar(self, evt):
        tc = self.GetWindow()
        key = evt.GetKeyCode()
        if (key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255):
            evt.Skip()
            return
        if chr(key).isdigit():
            evt.Skip()
            return

class UiApp(wx.App):
    def OnInit(self):
        # Call check_version here
        # check_version()

        # Initialize the frame
        # self.frame = TestPanel(parent=None, title="MCCI - Cricket UI")
        # self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        
        return True
    
    def CustInit(self):
        self.frame = TestPanel(parent=None, title="MCCI - Cricket UI")
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
    
def run():
    app = UiApp()
    app.CustInit()
    app.MainLoop()