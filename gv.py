# import graphviz as gv
# g = gv.Digraph(format='svg')
# g.edge('1','2')
# print g.render()

import wx
import wx.lib.floatcanvas.FloatCanvas as fc
import wx.lib.floatcanvas.NavCanvas as nc
app = wx.App()

main =wx.Frame(None,wx.ID_ANY,'main') ; main.Show()

nv = nc.NavCanvas(main)
cv = nv.Canvas

# box = cv.
# AddScaledTextBox("A Two Line\nString",
#                                       (40,70),2)
#                                       2,
#                                       Color = "Black",
#                                       BackgroundColor = None,
#                                       LineColor = "Red",
#                                       LineStyle = "Solid",
#                                       LineWidth = 1,
#                                       Width = None,
#                                       PadSize = 5,
#                                       Family = wx.ROMAN,
#                                       Style = wx.NORMAL,
#                                       Weight = wx.NORMAL,
#                                       Underlined = False,
#                                       Position = 'br',
#                                       Alignment = "left",
#                                       InForeground = False)

main.CreateStatusBar()

cv.Bind(fc.EVT_MOTION, lambda e:main.SetStatusText(str(e.Coords)))

cv.ZoomToBB()

app.MainLoop()