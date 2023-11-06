##############################################################################
# 
# Module: uiGlobal.py

##############################################################################
# Lib imports
import wx
import os
import requests
import webbrowser




IMG_ICON = "mcci_logo.ico"
IMG_LOGO = "mcci_logo.png"

ID_MENU_FILE_CLOSE  = 1012
ID_MENU_HELP_ABOUT = 1019
ID_MENU_HELP_WEB = 1017
ID_MENU_HELP_PORT = 1018
ID_MENU_HELP_PDB = 1020
ID_MENU_HELP_DNC = 1021
ID_ABOUT_IMAGE = 1033
ID_MENU_LOGIN = 1034

loginToken = None

root_Url = "https://www.cornellsaprun.com/dncserver/"
mcci_web = "https://mcci.com/"
mcci_support = "https://portal.mcci.com/portal/home"
brixui_dashboard = "https://www.cornellsaprun.com/grafana"
dncui = "https://www.cornellsaprun.com/dncui/"

##############################################################################

#======================================================================
# GLOBAL STRINGS
#======================================================================
VERSION_NAME  = "\nMCCI"+u"\u00AE"+" Brix UI"
VERSION_ID    = ""
VERSION_COPY  = "\nCopyright "+u"\u00A9"+" 2022 MCCI Corporation"

VERSION_STR = "v6.1.0"

repository_owner = "vinaynmcci"
repository_name = "swupdate"
###############################################################################


def check_version():
    
    api_url = f"https://api.github.com/repos/vinaynmcci/swupdate/releases/latest"
    response = requests.get(api_url)

    
    if response.status_code == 200:
        release_info = response.json()
        latest_version = release_info["tag_name"]

        if latest_version:
            if latest_version > VERSION_STR:
                app = wx.App(False)
                dlg = wx.MessageDialog(
                    None,
                    f"MCCI Cricket UI latest version ({latest_version}) is available \n" + "Please click on OK for more details",
                    "MCCI Cricket UI ",
                    style=wx.OK | wx.CANCEL | wx.ICON_INFORMATION,
                )
                result = dlg.ShowModal()
                if result == wx.ID_OK:
                    webbrowser.open("https://github.com/mcci-usb/COLLECTION-cricket-ui/releases/tag/v4.0.0")
                    dlg.Destroy()
                    # 
                elif result == wx.ID_NO:
                    # Implement action for clicking "No" here
                    pass
                dlg.Destroy()
            else:
                pass
                
                    
                
    else:
        print(f"Failed to retrieve information from GitHub. Status code: {response.status_code}")

check_version()

# if __name__ == "__main__":


class NumericValidator(wx.Validator):
    
    def __init__(self):
        
        wx.Validator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self, arg=None):
        print("Numarical validator")
       
        return NumericValidator()
   
    def Validate(self, win):
        
        # Returns the window associated with the validator.
        tc  = self.GetWindow()
        val = tc.GetValue()
        return val.isdigit()
   
    def OnChar(self, evt):
        
        # Returns the window associated with the validator.
        tc = self.GetWindow()
        key = evt.GetKeyCode()

        # For the case of delete and backspace, pass the key
        if (key == wx.WXK_BACK or key == wx.WXK_DELETE  or key > 255):
            evt.Skip()
            return
      
        elif (chr(key).isdigit() or chr(key) == "."):
            evt.Skip()
            return
    
    
    


        
        
