"""Palette displayed on the left side of main window."""

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


class Palette(tkinter.LabelFrame):
    """Palette displayed on the left side of main window."""

    def __init__(self, parent, main_window):
        """Initialize the palette."""
        super().__init__(parent, text="Výkres", padx=5, pady=5)
        self.main_window = main_window

        self.listbox = tkinter.Listbox(self)
        self.listbox.pack(fill=tkinter.BOTH, expand=True)
        self.group = tkinter.LabelFrame(self, text="Vybraná místnost",
                                        padx=5, pady=5)

        self.label_id_name = tkinter.Label(self.group, text="ID")
        self.label_id_name.grid(column=1, row=1, sticky="W")
        self.label_id_value = tkinter.Label(self.group, text="")
        self.label_id_value.grid(column=2, row=1, sticky="W")

        self.label_vertexes_name = tkinter.Label(self.group, text="Rohů")
        self.label_vertexes_name.grid(column=1, row=2, sticky="W")
        self.label_vertexes_value = tkinter.Label(self.group, text="")
        self.label_vertexes_value.grid(column=2, row=2, sticky="W")

        self.label_contour = tkinter.Label(self.group, text="Obrys")
        self.label_contour.grid(column=1, row=4, sticky="W")

        self.button1 = tkinter.Button(self.group, text="Smazat místnost ze seznamu",
                                      compound="left",
                                      command=self.delete_room_command,
                                      image=main_window.icons.edit_delete_shred_icon,
                                      width=200)
        self.button2 = tkinter.Button(self.group, text="Vymazat",
                                      compound="left",
                                      command=self.delete_room_polygon_command,
                                      image=main_window.icons.edit_delete_icon,
                                      height=28)
        self.button3 = tkinter.Button(self.group, text="Překreslit",
                                      compound="left",
                                      command=self.redraw_room_polygon_command,
                                      image=main_window.icons.edit_redo_icon,
                                      height=28)
        self.button4 = tkinter.Button(self.group, text="Vybrat polyčáru",
                                      compound="left",
                                      command=self.select_polygon_for_room,
                                      image=main_window.icons.rectangle,
                                      width=200, height=28)
        self.button1.grid(column=1, row=3, sticky="WE", columnspan=2)
        self.button2.grid(column=1, row=5, sticky="WE")
        self.button3.grid(column=2, row=5, sticky="WE")
        self.button4.grid(column=1, row=6, sticky="WE", columnspan=2)

        self.group.pack(fill=tkinter.X, expand=False)
        self.listbox.bind("<<ListboxSelect>>", self.on_room_click)
        self.disable_all()

    def enable_all(self):
        """Enable all buttons on palette."""
        self.button1.config(state="normal")
        self.button2.config(state="normal")
        self.button3.config(state="normal")
        self.button4.config(state="normal")

    def disable_all(self):
        """Disable all buttons on palette."""
        self.button1.config(state="disabled")
        self.button2.config(state="disabled")
        self.button3.config(state="disabled")
        self.button4.config(state="disabled")

    def fill_in_room_info(self, room):
        """Fill in information about the selected room."""
        self.label_id_value["text"] = room["room_id"]
        if room["polygon"] is not None and len(room["polygon"]) > 0:
            self.label_vertexes_value["text"] = len(room["polygon"])
            self.button2.config(state="normal")
            self.button3.config(text="Překreslit")
            self.button3.config(image=self.main_window.icons.edit_redo_icon)
        else:
            self.label_vertexes_value["text"] = "nenakresleno!"
            self.button2.config(state="disabled")
            self.button3.config(text="Nakreslit")
            self.button3.config(image=self.main_window.icons.edit_icon)

    def remove_all_rooms(self):
        """Remove all rooms from listbox."""
        self.listbox.delete(0, tkinter.END)

    def add_new_room(self, canvas_id):
        """Add a new room onto the listbox."""
        self.listbox.insert(tkinter.END, canvas_id)
        self.button2.config(state="normal")

    def get_selected_room(self):
        """Get the selected room (index+room ID)."""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            value = self.listbox.get(index)
            return index, value
        return None, None

    def find_room_index_in_list(self, room_id):
        """Find room specified by its ID on listbox."""
        size = self.listbox.size()
        for index in range(size):
            if room_id == self.listbox.get(index):
                return index
        return None

    def select_room_in_list(self, room):
        """Select room in listbox."""
        if room is not None:
            room_id = room["room_id"]
            index = self.find_room_index_in_list(room_id)
            if index is not None:
                self.listbox.activate(index)
                self.listbox.selection_clear(0, tkinter.END)
                self.listbox.selection_set(index)
        # activate(index)
        # @delete(first, last=None
        # get(first, last=None)
        # size()

    def on_room_click(self, event):
        """Handle event: room selected on listbox."""
        index, value = self.get_selected_room()
        if value:
            self.main_window.on_room_click_listbox(value)

    def delete_room_command(self):
        """Handle event: delete room button pressed."""
        index, value = self.get_selected_room()
        if value:
            self.main_window.delete_room_command(index, value)

    def delete_room_polygon_command(self):
        """Handle event: delete room polygon button pressed."""
        index, value = self.get_selected_room()
        if value:
            self.main_window.delete_room_polygon_command(index, value)

    def redraw_room_polygon_command(self):
        """Handle event: redraw room polygon command pressed."""
        index, value = self.get_selected_room()
        if value:
            self.main_window.redraw_room_polygon_command(index, value)

    def select_polygon_for_room(self):
        """Handle event: select polygon for room."""
        index, value = self.get_selected_room()
        if value:
            self.main_window.select_polygon_for_room(index, value)

    def delete_room_from_list(self, index):
        """Handle event: delete room from list."""
        self.listbox.selection_clear(0, tkinter.END)
        self.listbox.delete(index)
