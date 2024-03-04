"""Toolbar displayed on the main windo."""

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

from gui.dialogs.settings_dialog import SettingsDialog
from gui.dialogs.drawing_info_dialog import DrawingInfoDialog
from gui.dialogs.room_list_dialog import RoomListDialog
from gui.tooltip import Tooltip


class Toolbar(tkinter.LabelFrame):
    """Toolbar displayed on the main window."""

    def __init__(self, parent, main_window, canvas):
        """Initialize the toolbar."""
        super().__init__(parent, text="Nástroje", padx=5, pady=5)

        self.parent = parent
        self.main_window = main_window

        self.button_drawing_load = tkinter.Button(
            self, text="Otevřít výkres",
            image=main_window.icons.drawing_load_icon,
            command=main_window.open_drawing_command)

        Tooltip(self.button_drawing_load, "Načtení výkresu")

        self.button_drawing_save = tkinter.Button(
            self, text="Uložit výkres",
            image=main_window.icons.drawing_save_icon,
            command=main_window.save_drawing_command)

        Tooltip(self.button_drawing_save, "Uložení výkresu")

        self.button_file_open = tkinter.Button(
            self, text="Importovat místnosti",
            image=main_window.icons.file_open_icon,
            command=main_window.import_rooms_command)

        Tooltip(self.button_file_open, "Načtení místností ze souboru")

        self.button_file_save = tkinter.Button(
            self, text="Uložit místnosti",
            image=main_window.icons.file_save_icon,
            command=main_window.export_rooms_command)

        Tooltip(self.button_file_save, "Uložení místností do souboru")

        self.button_file_save_as = tkinter.Button(
            self, text="Uložit místnosti pod jiným jménem",
            image=main_window.icons.file_save_as_icon,
            command=main_window.export_rooms_as_command)

        Tooltip(self.button_file_save_as, "Uložení místností do souboru pod jiným jménem")

        self.button_sap_import_rooms = tkinter.Button(
            self, text="Seznam místností ze SAPu",
            image=main_window.icons.rooms_from_sap,
            command=main_window.import_rooms_from_sap)

        Tooltip(self.button_sap_import_rooms, "Přečtení seznamu místností ze SAPu")

        self.button_sap_sync_rooms = tkinter.Button(
            self, text="Synchronizace místností ze SAPem",
            image=main_window.icons.reload_icon,
            command=main_window.synchronize_rooms_with_sap)

        Tooltip(self.button_sap_sync_rooms, "Synchronizace místností ze SAPem")

        self.button_zoom_in = tkinter.Button(
            self, text="Zvětšit",
            image=main_window.icons.zoom_in_icon,
            command=main_window.zoom_plus)

        Tooltip(self.button_zoom_in, "Přiblížení výkresu")

        self.button_zoom_out = tkinter.Button(
            self, text="Zmenšit",
            image=main_window.icons.zoom_out_icon,
            command=main_window.zoom_minus)

        Tooltip(self.button_zoom_out, "Oddálení výkresu")

        self.button_zoom_11 = tkinter.Button(
            self, text="1:1",
            image=main_window.icons.zoom_original_icon,
            command=main_window.redraw)

        Tooltip(self.button_zoom_11, "Původní měřítko výkresu")

        self.button_view_grid = tkinter.Button(
            self, text="Mřížka",
            image=main_window.icons.view_grid_icon,
            command=canvas.toggle_grid)

        Tooltip(self.button_view_grid, "Zobrazení či skrytí mřížky")

        self.button_view_boundary = tkinter.Button(
            self, text="Okraj",
            image=main_window.icons.view_boundary_icon,
            command=canvas.toggle_boundary)

        Tooltip(self.button_view_boundary, "Zobrazení či skrytí okraje výkresu")

        self.button_drawing_info = tkinter.Button(
            self, text="Informace o výkresu",
            image=main_window.icons.drawing_info_icon,
            command=self.show_drawing_info_dialog)

        Tooltip(self.button_drawing_info, "Zobrazení informací o výkresu")

        self.button_room_list = tkinter.Button(
            self, text="Seznam místností",
            image=main_window.icons.room_list_icon,
            command=self.show_room_list_dialog)

        Tooltip(self.button_room_list, "Zobrazení seznamu místností")

        self.button_new_room = tkinter.Button(
            self, text="Nakreslit místnost",
            image=main_window.icons.edit_icon,
            command=self.main_window.palette.redraw_room_polygon_command)

        Tooltip(self.button_new_room, "Nakreslit místnost")

        self.button_new_room_polygon = tkinter.Button(
            self, text="Vybrat polyčáru pro místnost",
            image=main_window.icons.rectangle,
            command=self.main_window.palette.select_polygon_for_room)

        Tooltip(self.button_new_room_polygon, "Vybrat polyčáru pro místnost")

        # self.button_settings = tkinter.Button(
        #     self, text="Nastavení",
        #     image=main_window.icons.properties_icon,
        #     command=self.show_settings_dialog)

        self.button_quit = tkinter.Button(
            self, text="Ukončit",
            image=main_window.icons.exit_icon,
            command=main_window.quit)

        Tooltip(self.button_quit, "Ukončení aplikace")

        spacer1 = tkinter.Label(self, text="   ")
        spacer2 = tkinter.Label(self, text="   ")
        spacer3 = tkinter.Label(self, text="   ")
        spacer4 = tkinter.Label(self, text="   ")
        spacer5 = tkinter.Label(self, text="   ")
        spacer6 = tkinter.Label(self, text="   ")

        self.button_drawing_load.grid(column=1, row=1)
        self.button_drawing_save.grid(column=2, row=1)

        spacer1.grid(column=3, row=1)

        self.button_file_open.grid(column=4, row=1)
        self.button_file_save.grid(column=5, row=1)
        self.button_file_save_as.grid(column=6, row=1)

        spacer2.grid(column=7, row=1)

        self.button_sap_import_rooms.grid(column=8, row=1)
        self.button_sap_sync_rooms.grid(column=9, row=1)

        spacer3.grid(column=10, row=1)

        self.button_zoom_in.grid(column=11, row=1)
        self.button_zoom_out.grid(column=12, row=1)
        self.button_zoom_11.grid(column=13, row=1)
        self.button_view_grid.grid(column=14, row=1)
        self.button_view_boundary.grid(column=15, row=1)

        spacer4.grid(column=16, row=1)

        self.button_drawing_info.grid(column=17, row=1)
        self.button_room_list.grid(column=18, row=1)
        # self.button_settings.grid(column=19, row=1)

        spacer5.grid(column=20, row=1)

        self.button_new_room.grid(column=21, row=1)
        self.button_new_room_polygon.grid(column=22, row=1)

        spacer6.grid(column=23, row=1)
        self.button_quit.grid(column=24, row=1)

    def show_settings_dialog(self):
        """Show the settings dialog."""
        SettingsDialog(self.parent)

    def show_drawing_info_dialog(self):
        """Show the drawing info dialog."""
        DrawingInfoDialog(self.parent, self.main_window.drawing)

    def show_room_list_dialog(self):
        """Show the room list dialog."""
        RoomListDialog(self.parent, self.main_window.drawing)

    def disable_ui_items_for_no_drawing_mode(self):
        """Disable some buttons when application is set to no-drawing mode."""
        Toolbar.disable_button(self.button_drawing_save)
        Toolbar.disable_button(self.button_file_open)
        Toolbar.disable_button(self.button_file_save)
        Toolbar.disable_button(self.button_file_save_as)
        Toolbar.disable_button(self.button_sap_import_rooms)
        Toolbar.disable_button(self.button_sap_sync_rooms)
        Toolbar.disable_button(self.button_zoom_11)
        Toolbar.disable_button(self.button_zoom_in)
        Toolbar.disable_button(self.button_zoom_out)
        Toolbar.disable_button(self.button_view_grid)
        Toolbar.disable_button(self.button_view_boundary)
        Toolbar.disable_button(self.button_drawing_info)
        Toolbar.disable_button(self.button_room_list)
        Toolbar.disable_button(self.button_new_room)
        Toolbar.disable_button(self.button_new_room_polygon)

    def enable_ui_items_for_drawing_mode(self):
        """Enable some buttons when application is set to drawing mode."""
        Toolbar.enable_button(self.button_drawing_save)
        Toolbar.enable_button(self.button_file_open)
        Toolbar.enable_button(self.button_file_save)
        Toolbar.enable_button(self.button_file_save_as)
        Toolbar.enable_button(self.button_sap_import_rooms)
        Toolbar.enable_button(self.button_sap_sync_rooms)
        Toolbar.enable_button(self.button_zoom_11)
        Toolbar.enable_button(self.button_zoom_in)
        Toolbar.enable_button(self.button_zoom_out)
        Toolbar.enable_button(self.button_view_grid)
        Toolbar.enable_button(self.button_view_boundary)
        Toolbar.enable_button(self.button_drawing_info)
        Toolbar.enable_button(self.button_room_list)
        Toolbar.enable_button(self.button_new_room)
        Toolbar.enable_button(self.button_new_room_polygon)

    @staticmethod
    def disable_button(button):
        """Disable specified button on toolbar."""
        button['state'] = 'disabled'

    @staticmethod
    def enable_button(button):
        """Enable specified button on toolbar."""
        button['state'] = 'normal'
