"""Dialog to select areal, building, floor, and drawing."""

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


class DrawingSelectDialog(tkinter.Toplevel):
    """Dialog to select areal, building, floor, and drawing."""

    def __init__(self, parent, configuration):
        """Initialize the dialog."""
        tkinter.Toplevel.__init__(self, parent)
        self.title("Otevřít výkres")

        # don't display the dialog in list of opened windows
        self.transient(parent)

        label1 = tkinter.Label(self, text="Areál")
        label2 = tkinter.Label(self, text="Budova")
        label3 = tkinter.Label(self, text="Podlaží")
        label4 = tkinter.Label(self, text="Výkres")

        label1.grid(row=1, column=1, sticky="W", padx=5, pady=5)
        label2.grid(row=1, column=2, sticky="W", padx=5, pady=5)
        label3.grid(row=1, column=3, sticky="W", padx=5, pady=5)
        label4.grid(row=1, column=4, sticky="W", padx=5, pady=5)

        # close the dialog on 'x' click
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # get the focus
        self.grab_set()
