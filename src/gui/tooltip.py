"""Create a tooltip for a given widget."""

# taken from:
# https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter#36221216

import tkinter


class Tooltip(object):
    """Create a tooltip for a given widget."""

    def __init__(self, widget, text="widget info"):
        """Initialize the widget."""
        self.waittime = 500  # miliseconds
        self.wraplength = 180  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        """Handle the event: cursor pointer moves to the tooltip area."""
        self.schedule()

    def leave(self, event=None):
        """Handle the event: cursor pointer leaves the tooltip area."""
        self.unschedule()
        self.hidetip()

    def schedule(self):
        """Schedule time for displaying tooltip."""
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        """Unschedule time for displaying tooltip."""
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        """Show the tooltip on screen."""
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tkinter.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tkinter.Label(
            self.tw,
            text=self.text,
            justify="left",
            background="#ffffff",
            relief="solid",
            borderwidth=1,
            wraplength=self.wraplength,
        )
        label.pack(ipadx=1)

    def hidetip(self):
        """Hide the tooltip."""
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()
