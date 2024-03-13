"""Dialog with list of all rooms from drawing."""

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
from tkinter.scrolledtext import ScrolledText


class RoomListDialog(tkinter.Toplevel):
    """Dialog with list of all rooms from drawing."""

    def __init__(self, parent, drawing):
        """Initialize the dialog."""
        tkinter.Toplevel.__init__(self, parent)
        self.title("Seznam místností")

        rooms = drawing.rooms
        rooms_count = len(rooms)

        self.add_label(0, 0, "Počet místností")
        self.add_value_widget(0, 1, rooms_count)

        self.txt = ScrolledText(self, undo=True, tabs="4c 7c 10c 24c")
        self.txt.grid(row=1, column=0, columnspan=2, sticky="nwse", padx=2, pady=2)

        self.txt.tag_configure("underlined", underline=True)
        self.txt.tag_configure("blue", foreground="blue")
        self.txt.tag_configure("green", foreground="green")
        self.txt.tag_configure("red", foreground="red")

        self.txt.insert(tkinter.INSERT, "SAP ID\tgr.ID\tzakreslena\tsouřadnic\n", "underlined")

        for room in rooms:
            if "room_id" in room:
                self.txt.insert(tkinter.END, room["room_id"] + "\t", "blue")
            else:
                self.txt.insert(tkinter.END, "x\t", "red")

            if "canvas_id" in room and room["canvas_id"] is not None:
                self.txt.insert(tkinter.END, str(room["canvas_id"]) + "\t")
            else:
                self.txt.insert(tkinter.END, "x\t", "red")

            if room["polygon"] is not None and len(room["polygon"]) > 0:
                self.txt.insert(tkinter.END, "ano\t", "green")
            else:
                self.txt.insert(tkinter.END, "ne\t", "red")

            if room["polygon"] is not None:
                typ = "?"
                if "type" in room:
                    typ = room["type"]
                self.txt.insert(tkinter.END, str(len(room["polygon"])) + " (" + typ + ")\n")
            else:
                self.txt.insert(tkinter.END, "?\n")

        self.txt.configure(state="disabled")

        okButton = tkinter.Button(self, text="OK", command=self.ok)
        okButton.grid(row=2, column=0, sticky="WE")

        # close the dialog on 'x' click
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # get the focus
        self.grab_set()

        # how the buttons should behave
        self.bind("<Return>", lambda event: self.ok())
        self.bind("<Escape>", lambda event: self.destroy())

        # get the focus
        okButton.focus_set()

    def ok(self):
        """Handle event when Ok button is pressed."""
        self.destroy()

    def add_label(self, row, column, text):
        """Add a label to dialog."""
        label = tkinter.Label(self, text=text)
        label.grid(row=row, column=column, sticky="W", padx=5, pady=5)

    def add_value_widget(self, row, column, value):
        """Add a widget with value to dialog."""
        widget = self.value_widget(value)
        widget.grid(row=row, column=column, sticky="W", padx=5, pady=5)

    def value_widget(self, value):
        """Create new widget with value."""
        widget = tkinter.Entry(self)
        widget.insert(tkinter.END, value)
        widget.configure(state="readonly")
        return widget
