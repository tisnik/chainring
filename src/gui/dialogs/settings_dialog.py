"""Implementation of application settings dialog."""

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


class SettingsDialog(tkinter.Toplevel):
    """Implementation of application settings dialog."""

    def __init__(self, parent):
        """Initialize the dialog."""
        tkinter.Toplevel.__init__(self, parent)
        self.title("Nastavení")

        # don't display the dialog in list of opened windows
        self.transient(parent)

        self.group1 = tkinter.LabelFrame(self, text="Nastavení serveru", padx=5, pady=8)
        self.group2 = tkinter.LabelFrame(
            self, text="Informace o uživateli", padx=5, pady=8
        )
        self.group3 = tkinter.LabelFrame(self, text="Zobrazení výkresu", padx=5, pady=8)

        # frame group #1
        label1 = tkinter.Label(self.group1, text="Adresa")
        label2 = tkinter.Label(self.group1, text="Port")
        self.entryServerAddress = tkinter.Entry(self.group1)
        self.entryServerPort = tkinter.Entry(self.group1)

        label1.grid(row=1, column=1, sticky="W", padx=5, pady=5)
        label2.grid(row=2, column=1, sticky="W", padx=5, pady=5)
        self.entryServerAddress.grid(row=1, column=2, sticky="WE")
        self.entryServerPort.grid(row=2, column=2, sticky="WE")

        self.group1.grid(row=1, column=1, sticky="WE")

        # frame group #2
        label3 = tkinter.Label(self.group2, text="Uživatelské jméno")
        label3.grid(row=1, column=1, sticky="W", padx=5, pady=5)
        self.entryLogin = tkinter.Entry(self.group2)
        self.entryLogin.grid(row=1, column=2, sticky="WE")
        self.group2.grid(row=2, column=1, sticky="WE")

        # frame group #3
        label4 = tkinter.Label(self.group3, text="Barva pozadí")
        label5 = tkinter.Label(self.group3, text="Barva půdorysu")
        label6 = tkinter.Label(self.group3, text="Barva kreslení")
        label7 = tkinter.Label(self.group3, text="Barva místností")
        label8 = tkinter.Label(self.group3, text="Barva vybrané místnosti")
        label4.grid(row=1, column=1, sticky="W", padx=5, pady=5)
        label5.grid(row=2, column=1, sticky="W", padx=5, pady=5)
        label6.grid(row=3, column=1, sticky="W", padx=5, pady=5)
        label7.grid(row=4, column=1, sticky="W", padx=5, pady=5)
        label8.grid(row=5, column=1, sticky="W", padx=5, pady=5)
        self.group3.grid(row=3, column=1, sticky="WE")

        # rest
        okButton = tkinter.Button(self, text="OK", command=self.ok)
        okButton.grid(row=4, column=1, sticky="W")

        # close the dialog on 'x' click
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # get the focus
        self.grab_set()

        # how the buttons should behave
        self.bind("<Return>", lambda event: self.ok())
        self.bind("<Escape>", lambda event: self.destroy())

        # get the focus
        okButton.focus_set()

    def ok(self) -> None:
        """Handle Ok button press."""
        print("server address:", self.entryServerAddress.get())
        print("server port:", self.entryServerPort.get())
        print("username:", self.entryLogin.get())
        self.destroy()
