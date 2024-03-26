"""Status bar displayed in the main window."""

#
#  (C) Copyright 2017, 2018  Pavel Tisnovsky
#
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the Eclipse Public License v1.0
#  which accompanies this distribution, and is available at
#  http://www.eclipse.org/legal/epl-v10.html
#
#  Contributors:
#      Pavel Tisnovsky
#

import tkinter


class StatusBar(tkinter.Frame):
    """Status bar displayed in the main window."""

    def __init__(self, master: tkinter.Tk) -> None:
        """Initialize the class."""
        tkinter.Frame.__init__(self, master)
        self.label = tkinter.Label(self, bd=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
        self.label.pack(fill=tkinter.X)

    def set(self, format, *args):
        """Set status bar messages."""
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self) -> None:
        """Clear status bar content."""
        self.label.config(text="")
        self.label.update_idletasks()
