"""Implementation of help dialog."""

#
#  (C) Copyright 2017  Pavel Tisnovsky
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


class HelpDialog(tkinter.Toplevel):
    """Implementation of help dialog."""

    def __init__(self, parent):
        """Initialize the dialog."""
        tkinter.Toplevel.__init__(self, parent)
        self.title("Nápověda")
        self.transient(parent)

        f = tkinter.LabelFrame(self, text="x")

        scrollbar = tkinter.Scrollbar(f)
        text = tkinter.Text(f, height=5, width=60)

        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        text.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        scrollbar.config(command=text.yview)
        text.config(yscrollcommand=scrollbar.set)

        text.tag_configure("h1", font=("Arial", 20, "bold"))
        text.tag_configure("h2", font=("Arial", 16, "bold"))

        text.insert(tkinter.END, "Nápověda\n", "h1")
        text.insert(tkinter.END, "Import výkresu\n", "h2")
        text.insert(tkinter.END, "Získání místností ze SAPu\n", "h2")
        text.insert(tkinter.END, "Nakreslení místností\n", "h2")
        text.insert(tkinter.END, "Export výkresu do systému\n", "h2")

        help_message = """"""
        text.insert(tkinter.END, help_message)

        text.config(state=tkinter.DISABLED)
        f.grid(row=0, column=0, sticky="NWSE")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # rest
        okButton = tkinter.Button(self, text="OK", command=self.ok)
        okButton.grid(row=1, column=0, sticky="NWSE")

        # close the dialog on 'x' click
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def ok(self):
        """Handle Ok button press."""
        self.destroy()


def help():
    """Display help dialog on screen."""
    HelpDialog(None)
