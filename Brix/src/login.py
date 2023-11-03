
import time
import os
import threading
import wx
import pickle
import requests
from getpass import getpass
from uiGlobal import *
import uiMainApp

# Lib imports
import csv

# Own modules
from uiGlobal import *
import json
import shelve
import sys
import os
from pathlib import Path

class LogIn(wx.Frame):
    
    def __init__(self, parent, top):
        
        wx.Frame.__init__(self, parent = None, title = "Login BrixUI",
                           size = (260, 200))
        
        self.top = top
        self.uname = {}
        self.pswd = {}
        self.ldata = {}
        
        self.SetBackgroundColour("white")
        self.SetMinSize((260, 200))
        self.SetMaxSize((260, 200))
        self.panel = wx.Panel(self)

        self.top_vbox = wx.BoxSizer(wx.VERTICAL)
        self.login_vbox = wx.BoxSizer(wx.VERTICAL)
        #self.pswd_vbox = wx.BoxSizer(wx.VERTICAL)

        self.uname_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.pswd_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox_btn = wx.BoxSizer(wx.HORIZONTAL)
         
        self.st_uname = wx.StaticText(self, -1, "Username", size = (-1, -1))
        self.tc_uname = wx.TextCtrl(self, -1, "", size = (80, 20))

        self.st_pswd = wx.StaticText(self, -1, "Password", size = (-1, -1))
        self.tc_pswd = wx.TextCtrl(self, -1,"" ,size = (80, 20), style = wx.TE_PASSWORD)
        
        self.btnSet = wx.Button(self, -1, "Login", size =  (60,-1))
            
        self.uname_hbox.Add(self.st_uname, 0, flag=wx.ALIGN_RIGHT | wx.LEFT | 
                       wx.ALIGN_CENTER_VERTICAL, border=12)
        self.uname_hbox.Add(self.tc_uname, 0, flag=wx.ALIGN_CENTER_VERTICAL |
                       wx.LEFT, border = 18)
        #self.login_vbox.Add(self.uname_hbox, 0, wx.CENTER, 10)

        self.pswd_hbox.Add(self.st_pswd, 0, flag=wx.ALIGN_RIGHT | wx.LEFT | 
                       wx.ALIGN_CENTER_VERTICAL, border=12)
        self.pswd_hbox.Add(self.tc_pswd, 0, flag=wx.ALIGN_CENTER_VERTICAL |
                       wx.LEFT, border = 20)
        #self.login_vbox.Add(self.pswd_hbox, 0, wx.CENTER, 30)
        self.hbox_btn.Add(self.btnSet, 0, flag=wx.ALIGN_CENTER_VERTICAL |
                       wx.LEFT, border = 85)
        
        self.top_vbox.AddMany([
            (0,10,0),
            (self.uname_hbox, 1, wx.EXPAND | wx.ALL),
            (0,10,0),
            (self.pswd_hbox, 1, wx.EXPAND | wx.ALL),
            (0,10,0),
            (self.hbox_btn, 1, wx.EXPAND | wx.ALL),
            (0,10,0)
             ])
        
        self.btnSet.Bind(wx.EVT_BUTTON, self.onloginButton )

        #self.btnSetBind(wx.EVT_CLOSE, self.onloginButton )

        self.SetSizer(self.top_vbox)
        self.Centre()
        #self.panel.Fit()
        base = os.path.abspath(os.path.dirname(__file__))
        self.SetIcon(wx.Icon(base+"/icons/"+IMG_LOGO))
        self.Show()

        try:
            self.LoadDevice()
            
        except:
            self.ldata['port'] = None
            self.ldata['device'] = None

        self.tc_uname.SetValue(self.top.user) 

    def onloginButton(self, evt):
        
        
        username = self.tc_uname.GetValue()
        password = self.tc_pswd.GetValue()
        
        if username == '' or password == '':
            return False
        
        self.OnLogin(username,password)
        
    
    def OnLogin(self, username, password):
       
        payload = {"uname": username, "pwd" : password}
        resp = requests.post(root_Url + "login", data = payload)

        if(resp.status_code == 200):
            logResp =json.loads(resp.text)
            self.top.token = logResp["token"]
            self.top.Logwindow.write("user login successfully\n" )
            self.top.user = username
            self.top.SetStatusText("User Log In success")
            self.Destroy()
        elif(resp.status_code == 400):
            self.top.Logwindow.write("Invalid credentials\n" )
            self.tc_pswd.SetValue("")
        elif(resp.status_code == 502):
            self.top.Logwindow.write("Server unreachable\n" )
            self.Destroy()
        
        
        

        