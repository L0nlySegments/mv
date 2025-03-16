import wx

"""
              ..----.._    _
            .' .--.    "-.(O)_
'-.__.-'"'=:|  ,  _)_ \__ . c\'-..
             ''------'---''---'-"


             Müsli Virus v1.0
"""


IMAGE_PATH = 'maus.png'


class ShapedFrame(wx.Frame):
    def __init__(self):


        # Set up window frame
        wx.Frame.__init__(self, None, -1, 'm1', style= wx.FRAME_SHAPED | wx.SIMPLE_BORDER)
        self.hasShape = False


        # Load the image
        image = wx.Image(IMAGE_PATH, wx.BITMAP_TYPE_PNG)
        image.SetMaskColour(255, 255, 255)
        image.SetMask(True)
        self.bmp = wx.Bitmap(image)


        # Draw image to window
        self.SetClientSize((self.bmp.GetWidth(), self.bmp.GetHeight()))
        dc = wx.ClientDC(self)
        dc.DrawBitmap(self.bmp, 0, 0, True)


        self.SetWindowShape()


        # Bind event handlers
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_WINDOW_CREATE, self.SetWindowShape)




    def SetWindowShape(self):
        # Set the window shape to mause.jpeg's shape
        r = wx.Region(self.bmp)
        self.hasShape = self.SetShape(r)


    def OnPaint(self, evt=None):
        # Not exactly sure why this is needed, seems redundant ?
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0, True)




if __name__ == '__main__':
    app = wx.App()
    ShapedFrame().Show()
    app.MainLoop()
