"""Simple object oriented graphics library

The library is designed to make it very easy for novice programmers to
experiment with computer graphics in an object oriented fashion. It is
written by John Zelle for use with the book "Python Programming: An
Introduction to Computer Science" (Franklin, Beedle & Associates).

LICENSE: This is open-source software released under the terms of the
GPL (http://www.gnu.org/licenses/gpl.html).

PLATFORMS: The package is a wrapper around Tkinter and should run on
any platform where Tkinter is available.

INSTALLATION: Put this file somewhere where Python can see it.

OVERVIEW: There are two kinds of objects in the library. The GraphWin
class implements a window where drawing can be done and various
GraphicsObjects are provided that can be drawn into a GraphWin. As a
simple example, here is a complete program to draw a circle of radius
10 centered in a 100x100 window:

--------------------------------------------------------------------
from graphics import *

def main():
    win = GraphWin("My Circle", 100, 100)
    c = Circle(Point(50,50), 10)
    c.draw(win)
    win.getMouse() # Pause to view result
    win.close()    # Close window when done

main()
--------------------------------------------------------------------
GraphWin objects support coordinate transformation through the
setCoords method and pointer-based input through getMouse.

The library provides the following graphical objects:
    Point
    Line
    Circle
    Oval
    Rectangle
    Polygon
    Text
    Entry (for text-based input)
    Image

Various attributes of graphical objects can be set such as
outline-color, fill-color and line-width. Graphical objects also
support moving and hiding for animation effects.

The library also provides a very simple class for pixel-based image
manipulation, Pixmap. A pixmap can be loaded from a file and displayed
using an Image object. Both getPixel and setPixel methods are provided
for manipulating the image.

DOCUMENTATION: For complete documentation, see Chapter 4 of "Python
Programming: An Introduction to Computer Science" by John Zelle,
published by Franklin, Beedle & Associates.  Also see
http://mcsp.wartburg.edu/zelle/python for a quick reference"""
import time
import os

import tkinter as tk

##########################################################################
# Module Exceptions


class GraphicsError(Exception):
    """Generic error class for graphics module exceptions."""

    def __init__(self, *args):
        self.args = args

OBJ_ALREADY_DRAWN = "Object currently drawn"
UNSUPPORTED_METHOD = "Object doesn't support operation"
BAD_OPTION = "Illegal option value"
DEAD_THREAD = "Graphics thread quit unexpectedly"

_root = tk.Tk()
_root.withdraw()


def update():
    _root.update()

############################################################################
# Graphics classes start here


class GraphWin(tk.Canvas):
    """A GraphWin is a toplevel window for displaying graphics."""

    def __init__(self, title="Graphics Window",
                 width=200, height=200, autoflush=True):
        # Next line is a kludge fix to make it more likely
        # that a new window appears non-minimized.
        time.sleep(0.5)
        master = tk.Toplevel(_root)
        master.protocol("WM_DELETE_WINDOW", self.close)
        tk.Canvas.__init__(self, master, width=width, height=height)
        self.master.title(title)
        self.title = title
        self.pack()
        master.resizable(0, 0)
        self.foreground = "black"
        self.items = []
        self.mouseX = None
        self.mouseY = None
        self.key = None  # MB: added
        self.bind("<Button-1>", self._onClick)
        master.bind("<Key>", self._onKeyPress)  # MB: added
        self.height = height
        self.width = width
        self.autoflush = autoflush
        self._mouseCallback = None
        self._keyCallback = None  # MB: added
        self.trans = None
        self.closed = False
        if autoflush:
            _root.update()

    def __repr__(self):
        rep = 'GraphWin("{}", {}, {}, {})'
        return rep.format(self.title, self.getWidth(),
                           self.getHeight(), self.autoflush)

    # Including str explicitly overrides tk.Canvas's str method
    def __str__(self):
        return self.__repr__()

    def __checkOpen(self):
        if self.closed:
            raise GraphicsError("window is closed")

    def setBackground(self, color):
        """Set background color of the window"""
        self.__checkOpen()
        self.config(bg=color)
        self.__autoflush()

    def getBackground(self):
        """ Returns the background color of the window. """
        return self.cget('background')

    def setCoords(self, x1, y1, x2, y2):
        """Set coordinates of window to run from (x1,y1) in the
        lower-left corner to (x2,y2) in the upper-right corner."""
        self.trans = Transform(self.width, self.height, x1, y1, x2, y2)

    def close(self):
        """Close the window"""
        if self.closed:
            return
        self.closed = True
        self.master.destroy()
        self.__autoflush()

    def closeOnMouseClick(self):
        """
        Displays a message at the given bottom of the window
        telling the user to click the mouse when done,
        waits for a mouse click, and then closes the window
        when the user clicks the mouse.  See getMouseWithMessage
        for an extended version with similar functionality.
        """
        if not self.isClosed():
            xpos = self.width / 2
            ypos = self.height - 10
            bottom = Point(xpos, ypos)
            message = 'To exit, click anywhere in this window'
            text = Text(bottom, message)
            text.draw(self)

            try:
                self.getMouse()  # Wait for the user to click,

            # Attempting to getMouse in a closed window raises a
            # GraphicsError.  This is foolish if the window is about
            # to be closed but the user chose to close it manually
            # (using the X), so ignore such exceptions.
            except GraphicsError:
                pass

            self.close()  # then close the window

    def isClosed(self):
        return self.closed

    def __autoflush(self):
        if self.autoflush:
            _root.update()

    def plot(self, x, y, color="black"):
        """Set pixel (x,y) to the given color"""
        self.__checkOpen()
        xs, ys = self.toScreen(x, y)
        self.create_line(xs, ys, xs + 1, ys, fill=color)
        self.__autoflush()

    def plotPixel(self, x, y, color="black"):
        """Set pixel raw (independent of window coordinates) pixel
        (x,y) to color"""
        self.__checkOpen()
        self.create_line(x, y, x + 1, y, fill=color)
        self.__autoflush()

    def flush(self):
        """Update drawing to the window"""
        self.__checkOpen()
        self.update_idletasks()

    def getMouse(self):
        """
        Wait for the user to click the mouse and return the Point object
        that represents the point where the user clicked the mouse.

        For example, if the user clicks somewhere near the
        top middle of a window, then getMouse might return something
        like Point(200, 30).
        """
        self.update()  # flush any prior clicks
        self.mouseX = None
        self.mouseY = None
        while self.mouseX == None or self.mouseY == None:
            self.update()
            if self.isClosed():
                raise GraphicsError("getMouse in closed window")
            time.sleep(.1)  # give up thread
        x, y = self.toWorld(self.mouseX, self.mouseY)
        self.mouseX = None
        self.mouseY = None
        return Point(x, y)

    def getMouseWithMessage(self,
            message='To continue, click anywhere in this window',
            xpos=None,
            ypos=None,
            close_it=False,
            erase_it=True):
        """
        Displays a message at the bottom center of the window and
        waits for the user to click the mouse, then erases the message.

        Optional parameters let you:
          -- Display a different message
          -- Place the message at a different place in the window
               (xpos and ypos are as in Text)
          -- Close the window after the mouse is clicked
               (and ignore the GraphicsError that results if the user
               instead chooses to click the   X   in the window)
          -- NOT erase the message when done
        """
        if self.isClosed():
            return
        if xpos == None:
            xpos = self.width / 2
        if ypos == None:
            ypos = self.height - 10
        bottom = Point(xpos, ypos)
        text = Text(bottom, message)
        text.draw(self)

        try:
            self.getMouse()  # Wait for the user to click,

        # Attempting to getMouse in a closed window raises a
        # GraphicsError.  This is foolish if the window is about
        # to be closed but the user chose to close it manually
        # (using the X), so ignore such exceptions.
        except GraphicsError:
            if not close_it:
                raise

        if erase_it:
            text.undraw()
        if close_it:
            self.close()  # then close the window

    def checkMouse(self):
        """Return mouse click last mouse click or None if mouse has
        not been clicked since last call"""
        if self.isClosed():
            raise GraphicsError("checkMouse in closed window")
        self.update()
        if self.mouseX != None and self.mouseY != None:
            x, y = self.toWorld(self.mouseX, self.mouseY)
            self.mouseX = None
            self.mouseY = None
            return Point(x, y)
        else:
            return None

# MB: added
    def checkKey(self):
        """Return key or None if no key has
        been pressed since last call"""
        if self.isClosed():
            raise GraphicsError("checkKey in closed window")
        self.update()
        if self.key != None:
            keyToReturn = self.key
            self.key = None
            return keyToReturn
        else:
            return None
# MB: end

    def getHeight(self):
        """ Returns the height of the window. """
        return self.height

    def getWidth(self):
        """ Returns the width of the window. """
        return self.width

    def getTitle(self):
        """ Returns the title of the window. """
        return self.title

    def getAutoflush(self):
        """ Returns the 'autoflush' characteristic of the window. """
        return self.autoflush

    def toScreen(self, x, y):
        trans = self.trans
        if trans:
            return self.trans.screen(x, y)
        else:
            return x, y

    def toWorld(self, x, y):
        trans = self.trans
        if trans:
            return self.trans.world(x, y)
        else:
            return x, y

    def setMouseHandler(self, func):
        self._mouseCallback = func

    def _onClick(self, e):
        self.mouseX = e.x
        self.mouseY = e.y
        if self._mouseCallback:
            self._mouseCallback(Point(e.x, e.y))

    # MB: added
    def _onKeyPress(self, e):
        self.key = e.keysym
    # MB: end


class Transform:
    """Internal class for 2-D coordinate transformations"""

    def __init__(self, w, h, xlow, ylow, xhigh, yhigh):
        # w, h are width and height of window
        # (xlow,ylow) coordinates of lower-left [raw (0,h-1)]
        # (xhigh,yhigh) coordinates of upper-right [raw (w-1,0)]
        # xspan and yspan have now been stored to allow for repr calculations
        self.xspan = (xhigh - xlow)
        self.yspan = (yhigh - ylow)
        self.xbase = xlow
        self.ybase = yhigh
        self.xscale = self.xspan / float(w - 1)
        self.yscale = self.yspan / float(h - 1)

    def screen(self, x, y):
        # Returns x,y in screen (actually window) coordinates
        xs = (x - self.xbase) / self.xscale
        ys = (self.ybase - y) / self.yscale
        return int(xs + 0.5), int(ys + 0.5)

    def world(self, xs, ys):
        # Returns xs,ys in world coordinates
        x = xs * self.xscale + self.xbase
        y = self.ybase - ys * self.yscale
        return x, y

    def __repr__(self):
        w = (self.xscale + self.xspan) / self.xscale
        h = (self.yscale + self.yspan) / self.yscale
        ylow = self.ybase - self.yspan
        xhigh = self.xspan + self.xbase
        rep = 'Transform("{}, {}", {}, {}, {}, {})'
        return rep.format(w, h, self.xbase, ylow, xhigh, self.ybase)


# Default values for various item configuration options. Only a subset of
#   keys may be present in the configuration dictionary for a given item
DEFAULT_CONFIG = {"fill": "",
                  "outline": "black",
                  "width": "1",
                  "arrow": "none",
                  "text": "",
                  "justify": "center",
                  "font": ("helvetica", 12, "normal")}


class GraphicsObject:
    """Generic base class for all of the drawable objects"""
    # A subclass of GraphicsObject should override _draw and
    #   and _move methods.

    def __init__(self, options):
        # options is a list of strings indicating which options are
        # legal for this object.

        # When an object is drawn, canvas is set to the GraphWin(canvas)
        #    object where it is drawn and id is the TK identifier of the
        #    drawn shape.
        self.canvas = None
        self.id = None

        # config is the dictionary of configuration options for the widget.
        config = {}
        for option in options:
            config[option] = DEFAULT_CONFIG[option]
        self.config = config

    def setFill(self, color):
        """ Sets the interior color to the given argument. """
        self._reconfig("fill", color)

    def setOutline(self, color):
        """ Sets the outline color to the given argument. """
        self._reconfig("outline", color)

    def setWidth(self, width):
        """ Sets the line weight (width) to the given argument. """
        self._reconfig("width", width)

    def getFill(self):
        """ Returns the object's interior (fill) color. """
        return self.config['fill']

    def getOutline(self):
        """ Returns the object's outline color. """
        return self.config['outline']

    def getWidth(self):
        """ Returns the object's line weight (width). """
        return self.config['width']

    def draw(self, graphwin):
        """Draw the object in graphwin, which should be a GraphWin
        object.  A GraphicsObject may only be drawn into one
        window. Raises an error if attempt made to draw an object that
        is already visible."""

        if self.canvas and not self.canvas.isClosed():
            raise GraphicsError(OBJ_ALREADY_DRAWN)
        if graphwin.isClosed():
            raise GraphicsError("Can't draw to closed window")
        self.canvas = graphwin
        self.id = self._draw(graphwin, self.config)
        if graphwin.autoflush:
            _root.update()

    def undraw(self):
        """Undraw the object (i.e. hide it). Returns silently if the
        object is not currently drawn."""

        if not self.canvas:
            return
        if not self.canvas.isClosed():
            self.canvas.delete(self.id)
            if self.canvas.autoflush:
                _root.update()
        self.canvas = None
        self.id = None

    def move(self, dx, dy):
        """move object dx units in x direction and dy units in y
        direction"""
        self._move(dx, dy)
        canvas = self.canvas
        if canvas and not canvas.isClosed():
            trans = canvas.trans
            if trans:
                x = dx / trans.xscale
                y = -dy / trans.yscale
            else:
                x = dx
                y = dy
            self.canvas.move(self.id, x, y)
            if canvas.autoflush:
                _root.update()

    def _reconfig(self, option, setting):
        # Internal method for changing configuration of the object
        # Raises an error if the option does not exist in the config
        #    dictionary for this object
        if option not in self.config:
            raise GraphicsError(UNSUPPORTED_METHOD)
        options = self.config
        options[option] = setting
        if self.canvas and not self.canvas.isClosed():
            self.canvas.itemconfig(self.id, options)
            if self.canvas.autoflush:
                _root.update()

    def _draw(self, canvas, options):
        """draws appropriate figure on canvas with options provided
        Returns Tk id of item drawn"""
        pass  # must override in subclass

    def _move(self, dx, dy):
        """updates internal state of object to move it dx,dy units"""
        pass  # must override in subclass

    def __repr__(self):
        return "GraphicsObject(" + str(self.config) + ")"


class Point(GraphicsObject):
    def __init__(self, x, y):
        GraphicsObject.__init__(self, ["outline", "fill"])
        self.setFill = self.setOutline
        self.x = x
        self.y = y

    def _draw(self, canvas, options):
        x, y = canvas.toScreen(self.x, self.y)
        return canvas.create_rectangle(x, y, x + 1, y + 1, options)

    def _move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy

    def clone(self):
        other = Point(self.x, self.y)
        other.config = self.config.copy()
        return other

    def __repr__(self):
        return "Point(" + str(self.x) + "," + str(self.y) + ")"

    def getX(self):
        return self.x

    def getY(self):
        return self.y


class _BBox(GraphicsObject):
    # Internal base class for objects represented by bounding box
    # (opposite corners) Line segment is a degenerate case.

    def __init__(self, p1, p2, options=["outline", "width", "fill"]):
        GraphicsObject.__init__(self, options)
        self.p1 = p1.clone()
        self.p2 = p2.clone()

    def _move(self, dx, dy):
        self.p1.x = self.p1.x + dx
        self.p1.y = self.p1.y + dy
        self.p2.x = self.p2.x + dx
        self.p2.y = self.p2.y + dy

    def getP1(self):
        return self.p1.clone()

    def getP2(self):
        return self.p2.clone()

    def getCenter(self):
        p1 = self.p1
        p2 = self.p2
        return Point((p1.x + p2.x) / 2.0, (p1.y + p2.y) / 2.0)

    def __repr__(self):
        p1 = self.p1
        p2 = self.p2
        return repr(p1) + "," + repr(p2)


class Rectangle(_BBox):

    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2)

    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1, y1 = canvas.toScreen(p1.x, p1.y)
        x2, y2 = canvas.toScreen(p2.x, p2.y)
        return canvas.create_rectangle(x1, y1, x2, y2, options)

    def clone(self):
        other = Rectangle(self.p1, self.p2)
        other.config = self.config.copy()
        return other

    def __repr__(self):
        return "Rectangle(" + repr(self.p1) + "," + repr(self.p2) + ")"


class Oval(_BBox):

    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2)

    def clone(self):
        other = Oval(self.p1, self.p2)
        other.config = self.config.copy()
        return other

    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1, y1 = canvas.toScreen(p1.x, p1.y)
        x2, y2 = canvas.toScreen(p2.x, p2.y)
        return canvas.create_oval(x1, y1, x2, y2, options)

    def __repr__(self):
        return "Oval(" + repr(self.p1) + "," + repr(self.p2) + ")"


class Circle(Oval):

    def __init__(self, center, radius):
        p1 = Point(center.x - radius, center.y - radius)
        p2 = Point(center.x + radius, center.y + radius)
        Oval.__init__(self, p1, p2)
        self.radius = radius

    def clone(self):
        other = Circle(self.getCenter(), self.radius)
        other.config = self.config.copy()
        return other

    def getRadius(self):
        return self.radius

    def __repr__(self):
        center = Point(self.p1.x + self.radius, self.p1.y + self.radius)
        return "Circle(" + repr(center) + "," + str(self.radius) + ")"


class Line(_BBox):

    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2, ["arrow", "fill", "width"])
        self.setFill(DEFAULT_CONFIG['outline'])
        self.setOutline = self.setFill

    def clone(self):
        other = Line(self.p1, self.p2)
        other.config = self.config.copy()
        return other

    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1, y1 = canvas.toScreen(p1.x, p1.y)
        x2, y2 = canvas.toScreen(p2.x, p2.y)
        return canvas.create_line(x1, y1, x2, y2, options)

    def setArrow(self, option):
        """ Sets the lines' arrow style.
        The argument must be 'first' or 'last' or 'both' or 'none'. """
        if not option in ["first", "last", "both", "none"]:
            raise GraphicsError(BAD_OPTION)
        self._reconfig("arrow", option)

    def getArrow(self):
        """ Returns the line's arrow style. """
        return self.config['arrow']

    def __repr__(self):
        return "Line(" + repr(self.p1) + "," + repr(self.p2) + ")"


class Polygon(GraphicsObject):

    def __init__(self, *points):
        # if points passed as a list, extract it
        if len(points) == 1 and type(points[0] == type([])):
            points = points[0]
        self.points = list(map(Point.clone, points))
        GraphicsObject.__init__(self, ["outline", "width", "fill"])

    def clone(self):
        other = Polygon(*self.points)
        other.config = self.config.copy()
        return other

    def getPoints(self):
        return list(map(Point.clone, self.points))

    def _move(self, dx, dy):
        for p in self.points:
            p.move(dx, dy)

    def _draw(self, canvas, options):
        args = [canvas]
        for p in self.points:
            x, y = canvas.toScreen(p.x, p.y)
            args.append(x)
            args.append(y)
        args.append(options)
        return GraphWin.create_polygon(*args)

    def __repr__(self):
        points = self.points
        s = "Polygon(" + repr(points[0])
        for i, p in enumerate(points):
            if (i == 0):
                i = 1
                continue
            s = s + "," + repr(p)
        return s + ")"


class Text(GraphicsObject):

    def __init__(self, p, text):
        GraphicsObject.__init__(self, ["justify", "fill", "text", "font"])
        self.setText(text)
        self.anchor = p.clone()
        self.setFill(DEFAULT_CONFIG['outline'])
        self.setOutline = self.setFill

    def __repr__(self):
        rep = 'Text({}, "{}")'

        return rep.format(repr(self.anchor), self.getText())

    def _draw(self, canvas, options):
        p = self.anchor
        x, y = canvas.toScreen(p.x, p.y)
        return canvas.create_text(x, y, options)

    def _move(self, dx, dy):
        self.anchor.move(dx, dy)

    def clone(self):
        other = Text(self.anchor, self.config['text'])
        other.config = self.config.copy()
        return other

    def setText(self, text):
        self._reconfig("text", text)

    def getText(self):
        return self.config["text"]

    def getAnchor(self):
        return self.anchor.clone()

    def setFace(self, face):
        """ Sets the Text object's font type (aka face) to the given
        argument, which must be one of the following strings:
        'helvetica'   'arial'    'courier'    'times roman'. """
        if face in ['helvetica', 'arial', 'courier', 'times roman']:
            _dummy, s, b = self.config['font']
            self._reconfig("font", (face, s, b))
        else:
            raise GraphicsError(BAD_OPTION)

    def getFace(self):
        """ Returns the Text object's font type (e.g. 'arial'). """
        return self.config['font'][0]

    def setSize(self, size):
        """ Sets the Text Object's font size to the given argument.
        Values from 5 to 36, inclusive, are allowed. """
        if 5 <= size <= 36:
            f, _dummy, b = self.config['font']
            self._reconfig("font", (f, size, b))
        else:
            raise GraphicsError(BAD_OPTION)

    def getSize(self):
        """ Returns the Text object's font size (e.g. 12). """
        return self.config['font'][1]

    def setStyle(self, style):
        """ Sets the Text object's font style to the given argument,
        which must be one of the following strings:
           'bold'    'normal'    'italic'    'bold italic'. """
        if style in ['bold', 'normal', 'italic', 'bold italic']:
            f, s, _dummy = self.config['font']
            self._reconfig("font", (f, s, style))
        else:
            raise GraphicsError(BAD_OPTION)

    def getStyle(self):
        """ Returns the Text object's font style (e.g. 'bold'). """
        return self.config['font'][2]

    def setTextColor(self, color):
        """ Sets the Text object's text color to the given argument. """
        self.setFill(color)

    def getTextColor(self):
        """ Returns the Text object's text color. """
        return self.config['fill']


class Entry(GraphicsObject):

    def __init__(self, p, width):
        GraphicsObject.__init__(self, [])
        self.anchor = p.clone()
        # print self.anchor
        self.width = width
        self.text = tk.StringVar(_root)
        self.text.set("")
        self.fill = "gray"
        self.color = "black"
        self.font = DEFAULT_CONFIG['font']
        self.entry = None

    def __repr__(self):
        return "Entry(" + repr(self.anchor) + "," + str(self.width) + ")"

    def _draw(self, canvas, options):
        p = self.anchor
        x, y = canvas.toScreen(p.x, p.y)
        frm = tk.Frame(canvas.master)
        self.entry = tk.Entry(frm,
                              width=self.width,
                              textvariable=self.text,
                              bg=self.fill,
                              fg=self.color,
                              font=self.font)
        self.entry.pack()
        # self.setFill(self.fill)
        return canvas.create_window(x, y, window=frm)

    def getText(self):
        """ Returns the text currently in the Entry object. """
        return self.text.get()

    def _move(self, dx, dy):
        self.anchor.move(dx, dy)

    def getAnchor(self):
        return self.anchor.clone()

    def clone(self):
        other = Entry(self.anchor, self.width)
        other.config = self.config.copy()
        other.text = tk.StringVar()
        other.text.set(self.text.get())
        other.fill = self.fill
        return other

    def setText(self, t):
        """ Sets the Entry object to display the given string. """
        self.text.set(t)

    def setFill(self, color):
        """Sets the background color of the Entry to the given color."""
        self.fill = color
        if self.entry:
            self.entry.config(bg=color)

    def getFill(self, color):
        """ Returns the Entry object's background color. """
        return self.fill

    def _setFontComponent(self, which, value):
        font = list(self.font)
        font[which] = value
        self.font = tuple(font)
        if self.entry:
            self.entry.config(font=self.font)

    def setFace(self, face):
        """ Sets the Entry object's font type (aka face) to the given
        argument, which must be one of the following strings:
        'helvetica'   'arial'    'courier'    'times roman'. """
        if face in ['helvetica', 'arial', 'courier', 'times roman']:
            self._setFontComponent(0, face)
        else:
            raise GraphicsError(BAD_OPTION)

    def setSize(self, size):
        """ Sets the Text Object's font size to the given argument.
        Values from 5 to 36, inclusive, are allowed. """
        if 5 <= size <= 36:
            self._setFontComponent(1, size)
        else:
            raise GraphicsError(BAD_OPTION)

    def setStyle(self, style):
        """ Sets the Entry object's font style to the given argument,
        which must be one of the following strings:
           'bold'    'normal'    'italic'    'bold italic'. """
        if style in ['bold', 'normal', 'italic', 'bold italic']:
            self._setFontComponent(2, style)
        else:
            raise GraphicsError(BAD_OPTION)

    def setTextColor(self, color):
        """ Sets the Entry object's text color to the given argument."""
        self.color = color
        if self.entry:
            self.entry.config(fg=color)

    def getFace(self):
        """ Returns the Entry object's font type (e.g. 'arial'). """
        return self.font[0]

    def getSize(self):
        """ Returns the Entry object's font size (e.g. 12). """
        return self.font[1]

    def getStyle(self):
        """ Returns the Entry object's font style (e.g. 'bold'). """
        return self.font[2]

    def getTextColor(self):
        """ Returns the Entry object's text color. """
        return self.color


class Image(GraphicsObject):

    idCount = 0
    imageCache = {}  # tk photoimages go here to avoid GC while drawn

    def __init__(self, p, pixmap):
        GraphicsObject.__init__(self, [])
        self.anchor = p.clone()
        self.imageId = Image.idCount
        Image.idCount = Image.idCount + 1
        if type(pixmap) == type(""):
            self.img = tk.PhotoImage(file=pixmap, master=_root)
        else:
            self.img = pixmap.image

    def __repr__(self):
        return "Image(" + repr(self.anchor) + "," + repr(self.img) + ")"

    def _draw(self, canvas, options):
        p = self.anchor
        x, y = canvas.toScreen(p.x, p.y)
        self.imageCache[self.imageId] = self.img  # save a reference
        return canvas.create_image(x, y, image=self.img)

    def _move(self, dx, dy):
        self.anchor.move(dx, dy)

    def undraw(self):
        del self.imageCache[self.imageId]  # allow gc of tk photoimage
        GraphicsObject.undraw(self)

    def getAnchor(self):
        return self.anchor.clone()

    def clone(self):
        imgCopy = Pixmap(self.img.copy())
        other = Image(self.anchor, imgCopy)
        other.config = self.config.copy()
        return other

    def getPixmap(self):
        pm = Pixmap(0, 0)
        pm.image = self.img
        return pm


class Pixmap:
    """Pixmap represents an image as a 2D array of color values.
    A Pixmap can be made from a file (gif or ppm):
       pic = Pixmap("myPicture.gif")
    or initialized to a given size (initially transparent):
       pic = Pixmap(512, 512)
    """

    def __init__(self, *args):
        self.fileName = ""
        if len(args) == 1:  # a file name or pixmap
            self.fileName = args[0]
            if type(args[0]) == type(""):
                # self.image = _tkCall(tk.PhotoImage, file=args[0],
                #                      master=_root)
                self.image = tk.PhotoImage(file=args[0], master=_root)
            else:
                self.image = args[0]
        else:  # arguments are width and height
            width, height = args
            # self.image = _tkCall(tk.PhotoImage, master=_root,
            #                      width=width, height=height)
            self.image = tk.PhotoImage(master=_root, width=width,
                                       height=height)

    def __repr__(self):
        if (self.fileName == ""):
            rep = 'Pixmap("{},{})'
            return rep.format(tk.StringVar(self.image.width),
                              tk.StringVar(self.image.height))
        return 'Pixmap("{}")'.format(self.fileName)

    def getWidth(self):
        """Returns the width of the image in pixels"""
        return self.image.width()  # _tkCall(self.image.width)

    def getHeight(self):
        """Returns the height of the image in pixels"""
        return self.image.height()  # _tkCall(self.image.height)

    def getPixel(self, x, y):
        """Returns a list [r,g,b] with the RGB color values for pixel (x,y)
        r,g,b are in range(256)

        """

        value = self.image.get(x, y)  # _tkCall(self.image.get, x,y)
        if type(value) == type(0):
            return [value, value, value]
        else:
            return list(map(int, value.split()))

    def setPixel(self, x, y, rgbTuple):
        """Sets pixel (x,y) to the color given by r,g,b values in rgbTuple.
        r,g,b should be in range(256)

        """

        # _tkExec(self.image.put, "{" + color_rgb(*rgbTuple) +"}", (x, y))
        self.image.put("{" + color_rgb(*rgbTuple) + "}", (x, y))

    def clone(self):
        """Returns a copy of this Pixmap"""
        return Pixmap(self.image.copy())

    def save(self, filename):
        """Saves the pixmap image to filename.
        The format for the save image is determined from the filname extension.
        """
        _dummy, name = os.path.split(filename)
        ext = name.split(".")[-1]
        # _tkExec(self.image.write, filename, format=ext)
        self.image.write(filename, format=ext)


def color_rgb(r, g, b):
    """r,g,b are intensities of red, green, and blue in range(256)
    Returns color specifier string for the resulting color"""
    return "#%02x%02x%02x" % (r, g, b)


def test():
    window = GraphWin('My first Zellegraphics window', 700, 400)

    center_point = Point(300, 100)

    circle = Circle(center_point, 50)
    circle.setFill('green')
    circle.draw(window)

    window.getMouseWithMessage(ypos=20, xpos=500)

    circle.setFill('blue')
    window.closeOnMouseClick()

#     win = GraphWin("hello")
#     win.setCoords(0, 0, 10, 10)
#     t = Text(Point(5, 5), "Centered Text")
#     t.draw(win)
#     p = Polygon(Point(1, 1), Point(5, 3), Point(2, 7))
#     p.draw(win)
#     e = Entry(Point(5, 6), 10)
#     e.draw(win)
#     win.getMouse()
#     p.setFill("red")
#     p.setOutline("blue")
#     p.setWidth(2)
#     s = ""
#     for pt in p.getPoints():
#         s = s + "(%0.1f,%0.1f) " % (pt.getX(), pt.getY())
#     t.setText(e.getText())
#     e.setFill("green")
#     e.setText("Spam!")
#     e.move(2, 0)
#     win.getMouse()
#
#     p.move(2, 3)
#     s = ""
#     for pt in p.getPoints():
#         s = s + "(%0.1f,%0.1f) " % (pt.getX(), pt.getY())
#     t.setText(s)
#     win.getMouse()
#     p.undraw()
#     e.undraw()
#     t.setStyle("bold")
#     win.getMouse()
#     t.setStyle("normal")
#     win.getMouse()
#     t.setStyle("italic")
#     win.getMouse()
#     t.setStyle("bold italic")
#     win.getMouse()
#     t.setSize(14)
#     win.getMouse()
#     t.setFace("arial")
#     t.setSize(20)
#     win.closeOnMouseClick()

if __name__ == "__main__":
    test()
