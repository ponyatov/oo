## @file
## @brief GUI egnine /wxPython/

import sys
import wx
import threading

## GUI thread
class GUI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        ## wx application
        self.app = wx.App()
        ##
        self.frame = wx.Frame(None,wx.ID_ANY,str(sys.argv))
    def run(self):
        self.frame.Show()
        self.app.MainLoop()

gui = GUI()

if __name__ == "__main__":
    gui.start()
    gui.join()
