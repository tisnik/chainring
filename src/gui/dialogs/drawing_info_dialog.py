"""Implementation of dialog with drawing info."""

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

from entities.drawing_entity_type import DrawingEntityType


class DrawingInfoDialog(tkinter.Toplevel):
    """Implementation of dialog with drawing info."""

    def __init__(self, parent, drawing):
        """Initialize the class with configuration dialog."""
        tkinter.Toplevel.__init__(self, parent)
        self.title("Informace o výkresu")

        drawing_statistic = drawing.statistic
        rooms_count = len(drawing.rooms)

        # don't display the dialog in list of opened windows
        self.transient(parent)

        group0 = tkinter.LabelFrame(self, text="ID výkresu", padx=5, pady=5)
        group0.grid(row=0, column=1, padx=5, pady=5, sticky="WE")

        # display drawing ID
        DrawingInfoDialog.add_value_widget(
            group0, 1, 1, drawing.drawing_id or "Nezadáno!"
        )

        group1 = tkinter.LabelFrame(self, text="Grafické entity", padx=5, pady=5)
        group1.grid(row=1, column=1, padx=5, pady=5, sticky="WE")

        DrawingInfoDialog.add_label(group1, 1, 1, "Úseček")
        DrawingInfoDialog.add_label(group1, 2, 1, "Kružnic")
        DrawingInfoDialog.add_label(group1, 3, 1, "Oblouků")
        DrawingInfoDialog.add_label(group1, 4, 1, "Textů")
        DrawingInfoDialog.add_label(group1, 5, 1, "Polyčar")
        DrawingInfoDialog.add_label(group1, 7, 1, "Celkem")

        DrawingInfoDialog.add_value_widget(
            group1, 1, 2, drawing_statistic[DrawingEntityType.LINE]
        )

        DrawingInfoDialog.add_value_widget(
            group1, 2, 2, drawing_statistic[DrawingEntityType.CIRCLE]
        )

        DrawingInfoDialog.add_value_widget(
            group1, 3, 2, drawing_statistic[DrawingEntityType.ARC]
        )

        DrawingInfoDialog.add_value_widget(
            group1, 4, 2, drawing_statistic[DrawingEntityType.TEXT]
        )

        DrawingInfoDialog.add_value_widget(
            group1, 5, 2, drawing_statistic[DrawingEntityType.POLYLINE]
        )

        lbl = tkinter.Label(group1, text="")
        lbl.grid(row=6, column=1, columnspan=2, sticky="WE")

        DrawingInfoDialog.add_value_widget(
            group1, 7, 2, DrawingInfoDialog.compute_sum(drawing_statistic)
        )

        group2 = tkinter.LabelFrame(self, text="Místnosti", padx=5, pady=5)
        group2.grid(row=2, column=1, padx=5, pady=5, sticky="WE")

        DrawingInfoDialog.add_label(group2, 1, 1, "Počet místností")
        DrawingInfoDialog.add_value_widget(group2, 1, 2, rooms_count)

        okButton = tkinter.Button(self, text="OK", command=self.ok)
        okButton.grid(row=3, column=1, sticky="WE")

        # close the dialog on 'x' click
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # get the focus
        self.grab_set()

        # how the buttons should behave
        self.bind("<Return>", lambda event: self.ok())
        self.bind("<Escape>", lambda event: self.destroy())

        # get the focus
        okButton.focus_set()

    @staticmethod
    def add_label(container, row, column, text):
        """Add a label to dialog."""
        label = tkinter.Label(container, text=text)
        label.grid(row=row, column=column, sticky="W", padx=5, pady=5)

    @staticmethod
    def add_value_widget(container, row, column, value):
        """Create a widget with value to dialog."""
        widget = DrawingInfoDialog.value_widget(container, value)
        widget.grid(row=row, column=column, sticky="W", padx=5, pady=5)

    @staticmethod
    def value_widget(container, value):
        """Add a widget with value to dialog."""
        widget = tkinter.Entry(container)
        widget.insert(tkinter.END, value)
        widget.configure(state="readonly")
        return widget

    def ok(self):
        """Handle the Ok button press."""
        self.destroy()

    @staticmethod
    def compute_sum(drawing_statistic):
        """Compute summary of all values specified."""
        return sum(drawing_statistic.values())
