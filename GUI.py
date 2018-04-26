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
        ## main window
        self.frame = wx.Frame(None,wx.ID_ANY,str(sys.argv))
        ## menu
        self.menubar = wx.MenuBar()
        ## file
        self.file = wx.Menu()
        self.menubar.Append(self.file,'&File')
        ## file/exit
        self.exit = self.file.Append(wx.ID_EXIT,'E&xit')
        ## help
        self.help = wx.Menu()
        self.menubar.Append(self.help,'&Help')
        ## help/about
        self.help.Append(wx.ID_ABOUT,'&About\tF1')
    def run(self):
        self.frame.SetMenuBar(self.menubar)
        self.frame.Show()
        self.app.MainLoop()

gui = GUI()

if __name__ == "__main__":
    gui.start()
    gui.join()
