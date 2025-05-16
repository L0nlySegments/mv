import wx, binascii, time
from res import MAUS_HEX
from tempfile import gettempdir

"""
              ..----.._    _
            .' .--.    "-.(O)_
'-.__.-'"'=:|  ,  _)_ /__ . c\'-..
             ''------'---''---'-"


             Müsli Virus v1.0
"""

class ShapedFrame(wx.Frame):
    def __init__(self, path):
        # Set up window frame
        wx.Frame.__init__(self, None, -1, '', style= wx.FRAME_SHAPED | wx.SIMPLE_BORDER | wx.STAY_ON_TOP)
        self.hasShape = False

        # Load the image
        image = wx.Image(path, wx.BITMAP_TYPE_PNG)
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
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)

    def SetWindowShape(self):
        # Set the window shape to mause.jpeg's shape
        r = wx.Region(self.bmp)
        self.hasShape = self.SetShape(r)


    def OnPaint(self, evt=None):
        # Not exactly sure why this is needed, seems redundant ?
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0, True)

    def OnLeftDown(self, evt):
        self.CaptureMouse()
        pos = self.ClientToScreen(evt.GetPosition())
        origin = self.GetPosition()
        self.delta = wx.Point(pos.x - origin.x, pos.y - origin.y)

    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            pos = self.ClientToScreen(evt.GetPosition())
            pos_w = self.GetPosition()
            newPos = (pos.x - self.delta.x, pos.y - self.delta.y)
            self.Move(newPos)
    
    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()

class MainApp(wx.App):
    def __init__(self, img_path, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        self.img_path = img_path
        super().__init__(redirect, filename, useBestVisual, clearSigInt)

    def MainLoop(self):
        # Create an event loop and make it active.  If you are
        # only going to temporarily have a nested event loop then
        # you should get a reference to the old one and set it as
        # the active event loop when you are done with this one...
        evtloop = wx.GUIEventLoop()
        old = wx.EventLoop.GetActive()
        wx.EventLoop.SetActive(evtloop)

        while self.keepGoing:
            # At this point in the outer loop you could do
            # whatever you implemented your own MainLoop for.  It
            # should be quick and non-blocking, otherwise your GUI
            # will freeze.

            # This inner loop will process any GUI events
            # until there are no more waiting.
            while evtloop.Pending():
                evtloop.Dispatch()

            # Send idle events to idle handlers.  You may want to
            # throttle this back a bit somehow so there is not too
            # much CPU time spent in the idle handlers.  For this
            # example, I'll just snooze a little...
            time.sleep(0.10)
            evtloop.ProcessIdle()
        wx.EventLoop.SetActive(old)

    def OnInit(self):
        self.frame = ShapedFrame(path=self.img_path)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)

        self.keepGoing = True
        return True

if __name__ == '__main__':
    # Write maus.hex to temp directory
    temp_img = f'{gettempdir()}/maus.png'
    with open(temp_img, 'wb') as image_file:
        image_file.write(binascii.unhexlify(MAUS_HEX))

    app = MainApp(temp_img)
    app.MainLoop()

