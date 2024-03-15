"""Dialogs used to load various data into the application."""

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

import time
import tkinter
from tkinter import filedialog, messagebox

from draw_service import DrawServiceInterface


class RoomsFromSapDialog(tkinter.Toplevel):
    """Dialog to import rooms from SAP."""

    def calendar_part(self):
        """Initialize the dialog."""
        top_part = tkinter.LabelFrame(self, text="Datum platnosti", padx=5, pady=5)
        top_part.grid(row=1, column=1, sticky="NWSE")

        label = tkinter.Label(top_part, text="Platnost od")
        label.grid(row=1, column=1, sticky="W", padx=5, pady=5)

        self.calendar = tkinter.Entry(top_part, width=12)
        today = time.strftime("%Y-%m-%d")
        self.calendar.insert(tkinter.END, today)
        self.calendar.grid(row=1, column=2, sticky="W", padx=5, pady=5)

        label = tkinter.Label(top_part, text="(rok-měsíc-den)")
        label.grid(row=2, column=2, sticky="W", padx=5, pady=5)

        label = tkinter.Label(top_part, text="ID výkresu")
        label.grid(row=1, column=4, sticky="W", padx=5, pady=5)

        self.id = tkinter.StringVar()
        self.id_entry = tkinter.Entry(top_part, width=20, state="readonly", textvariable=self.id)
        self.id_entry.grid(row=1, column=5, sticky="W", padx=5, pady=5)

        listArealsButton = tkinter.Button(top_part, text="Načíst seznam areálů",
                                          command=self.read_areals)
        listArealsButton.grid(row=1, column=3, sticky="WE")

    def command_part(self):
        """Bottom part of dialog: buttons."""
        bottom_part = tkinter.LabelFrame(self, text="Operace", padx=5, pady=5)
        bottom_part.grid(row=3, column=1, sticky="NWSE")

        self.okButton = tkinter.Button(bottom_part, text="OK", width=10, command=self.ok)
        self.okButton.grid(row=5, column=1, sticky="WE")

        self.cancelButton = tkinter.Button(bottom_part, text="Storno", width=10,
                                           command=self.cancel)
        self.cancelButton.grid(row=5, column=2, sticky="WE")

    def aoid_part(self):
        """Middle part of dialog: lists of AOIDs."""
        middle_part = tkinter.LabelFrame(self, text="Výběr podlaží", padx=5, pady=5)
        middle_part.grid(row=2, column=1, sticky="NWSE")

        label = tkinter.Label(middle_part, text="Areály")
        label.grid(row=1, column=1, sticky="W", padx=5, pady=5)
        label = tkinter.Label(middle_part, text="Budovy")
        label.grid(row=1, column=2, sticky="W", padx=5, pady=5)
        label = tkinter.Label(middle_part, text="Podlaží")
        label.grid(row=1, column=3, sticky="W", padx=5, pady=5)
        label = tkinter.Label(middle_part, text="Místnosti")
        label.grid(row=1, column=4, sticky="W", padx=5, pady=5)

        frame1 = tkinter.Frame(middle_part)
        scrollbar1 = tkinter.Scrollbar(frame1, orient=tkinter.VERTICAL)
        self.arealList = tkinter.Listbox(frame1, height=20, width=30, yscrollcommand=scrollbar1.set)
        self.arealList.bind("<<ListboxSelect>>", lambda event: self.on_areal_select(event))
        scrollbar1.config(command=self.arealList.yview)
        scrollbar1.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.arealList.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        frame1.grid(row=2, column=1, sticky="NWSE")

        frame2 = tkinter.Frame(middle_part)
        scrollbar2 = tkinter.Scrollbar(frame2, orient=tkinter.VERTICAL)
        self.buildingList = tkinter.Listbox(frame2, height=20, width=30,
                                            yscrollcommand=scrollbar2.set)
        self.buildingList.bind("<<ListboxSelect>>", lambda event: self.on_building_select(event))
        scrollbar2.config(command=self.buildingList.yview)
        scrollbar2.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.buildingList.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        frame2.grid(row=2, column=2, sticky="NWSE")

        frame3 = tkinter.Frame(middle_part)
        scrollbar3 = tkinter.Scrollbar(frame3, orient=tkinter.VERTICAL)
        self.floorList = tkinter.Listbox(frame3, height=20, width=30, yscrollcommand=scrollbar3.set)
        self.floorList.bind("<<ListboxSelect>>", lambda event: self.on_floor_select(event))
        scrollbar3.config(command=self.floorList.yview)
        scrollbar3.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.floorList.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        frame3.grid(row=2, column=3, sticky="NWSE")

        frame4 = tkinter.Frame(middle_part)
        scrollbar4 = tkinter.Scrollbar(frame4, orient=tkinter.VERTICAL)
        self.roomList = tkinter.Listbox(frame4, height=20, width=30, yscrollcommand=scrollbar4.set)
        scrollbar4.config(command=self.floorList.yview)
        scrollbar4.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.roomList.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        frame4.grid(row=2, column=4, sticky="NWSE")

    def __init__(self, parent, configuration):
        """Initialize the dialog for importing rooms from SAP."""
        tkinter.Toplevel.__init__(self, parent)

        self.parent = parent
        self.configuration = configuration
        self.address = self.configuration.server_address
        self.port = self.configuration.server_port

        self.areals = None
        self.buildings = None
        self.floors = None
        self.rooms = None

        if self.address and self.port:
            self.url = DrawServiceInterface.get_url(self.address, self.port)

        self.drawServiceInterface = DrawServiceInterface(service_url=self.url)

        self.title("Import místností ze SAPu")

        self.calendar_part()
        self.aoid_part()
        self.command_part()

        # close the dialog on 'x' click
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # get the focus
        self.grab_set()

        # how the buttons should behave
        self.bind("<Return>", lambda event: self.ok())
        self.bind("<Escape>", lambda event: self.destroy())

    def show(self):
        """Show the dialog on screen."""
        self.wm_deiconify()
        self.wait_window()
        return self.rooms, self.id.get()

    def list_box_index(self, event):
        """Handle event when item is selected from list box."""
        widget = event.widget
        selection = widget.curselection()
        if selection:
            return int(selection[0])
        return None

    def on_areal_select(self, event):
        """Handle event when areal is selected from list box."""
        index = self.list_box_index(event)
        if index is not None:
            areal = self.areals[index]
            if areal and "AOID" in areal:
                aoid = areal["AOID"]
                self.read_buildings(aoid)

    def on_building_select(self, event):
        """Handle event when building is selected from list box."""
        index = self.list_box_index(event)
        if index is not None:
            building = self.buildings[index]
            if building and "AOID" in building:
                aoid = building["AOID"]
                self.read_floors(aoid)

    def on_floor_select(self, event):
        """Handle event when floor is selected from list box."""
        index = self.list_box_index(event)
        if index is not None:
            floor = self.floors[index]
            if floor and "AOID" in floor:
                aoid = floor["AOID"]
                self.read_rooms(aoid)
                full_id = aoid.replace(".", "_").replace("/", "_")
                valid_from = self.calendar.get().replace("_", "").replace("-", "")
                self.id.set("{d}_{v}".format(d=full_id, v=valid_from))

    def fill_in_listbox(self, listbox, data):
        """Fill in specified list box with provided data."""
        listbox.delete(0, tkinter.END)
        for item in data:
            val = "{name} ({aoid})".format(name=item["Label"], aoid=item["AOID"])
            listbox.insert(tkinter.END, val)

    def error_server_address(self):
        """Show error message when server is not configured properly."""
        messagebox.showerror("Nastala chyba", "Není nastavená adresa serveru")

    def error_server_call(self, message):
        """Show error message when server is not responding."""
        messagebox.showerror("Nastala chyba", "Nastala chyba: {e}".format(e=message))

    def read_areals(self):
        """Read list of areals from SAP."""
        valid_from = self.calendar.get()
        if not self.url:
            self.error_server_address()
            return
        data, message = self.drawServiceInterface.read_areals(valid_from)
        if data:
            self.areals = data
            self.fill_in_listbox(self.arealList, data)
        else:
            self.error_server_call(message)

    def read_buildings(self, aoid):
        """Read list of buildings from SAP."""
        valid_from = self.calendar.get()
        if not self.url:
            self.error_server_address()
            return
        data, message = self.drawServiceInterface.read_buildings(valid_from, aoid)
        if data:
            self.buildings = data
            self.fill_in_listbox(self.buildingList, data)
        else:
            self.error_server_call(message)

    def read_floors(self, aoid):
        """Read list of floors from SAP."""
        valid_from = self.calendar.get()
        if not self.url:
            self.error_server_address()
            return
        data, message = self.drawServiceInterface.read_floors(valid_from, aoid)
        if data:
            self.floors = data
            self.fill_in_listbox(self.floorList, data)
        else:
            self.error_server_call(message)

    def read_rooms(self, aoid):
        """Read list of rooms from SAP."""
        valid_from = self.calendar.get()
        if not self.url:
            self.error_server_address()
            return
        data, message = self.drawServiceInterface.read_rooms(valid_from, aoid)
        if data:
            self.rooms = data
            self.fill_in_listbox(self.roomList, data)
        else:
            self.error_server_call(message)

    def ok(self):
        """Handle the Ok button press."""
        self.destroy()

    def cancel(self):
        """Handle the Cancel button press."""
        self.rooms = None
        self.destroy()


class LoadDialogs:
    """Dialogs used to load various data into the application."""

    @staticmethod
    def load_drawing(root):
        """Dialog shown to select drawing to import."""
        filetypes = [("Výkresy", "*.drw"),
                     ("Výkresy z CADu", "*.dxf")]
        dialog = filedialog.Open(root, filetypes=filetypes)
        return dialog.show()

    @staticmethod
    def load_rooms(root):
        """Dialog shown to select rooms to import from file."""
        filetypes = [("Místnosti", "*.rooms")]
        dialog = filedialog.Open(root, filetypes=filetypes)
        return dialog.show()

    @staticmethod
    def load_rooms_from_sap(root, configuration):
        """Dialog shown to select rooms to import from SAP."""
        return RoomsFromSapDialog(root, configuration).show()
