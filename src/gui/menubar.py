"""Menu bar displayed on the main window."""

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
from tkinter import messagebox

from draw_service import DrawServiceInterface
from gui.dialogs.about_dialog import about
from gui.dialogs.configure import configure
from gui.dialogs.drawing_info_dialog import DrawingInfoDialog
from gui.dialogs.room_list_dialog import RoomListDialog
from gui.dialogs.settings_dialog import SettingsDialog


class Menubar(tkinter.Menu):
    """Menu bar displayed on the main window."""

    def __init__(self, parent, main_window, canvas):
        """Initialize the menu bar."""
        super().__init__(tearoff=0)

        self.parent = parent
        self.main_window = main_window

        self.filemenu = tkinter.Menu(self, tearoff=0)
        self.filemenu.add_command(label="Otevřít výkres",
                                  image=main_window.icons.drawing_load_icon,
                                  compound="left", underline=0, accelerator="Ctrl+O",
                                  command=main_window.open_drawing_command)

        self.filemenu.add_command(label="Uložit výkres",
                                  image=main_window.icons.drawing_save_icon,
                                  compound="left", underline=0, accelerator="Ctrl+S",
                                  command=main_window.save_drawing_command)

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Export výkresu na server",
                                  image=main_window.icons.server,
                                  compound="left", underline=0,
                                  command=main_window.send_drawing_to_server)

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Konec", image=main_window.icons.exit_icon,
                                  compound="left", underline=0, accelerator="Ctrl+Q",
                                  command=parent.quit)

        self.rooms = tkinter.Menu(self, tearoff=0)

        self.rooms.add_command(label="Seznam místností",
                               image=main_window.icons.room_list_icon,
                               compound="left", underline=0,
                               command=self.show_room_list_dialog,
                               accelerator="Ctrl+M")

        self.rooms.add_separator()

        self.rooms.add_command(label="Importovat místnosti",
                               image=main_window.icons.file_open_icon,
                               compound="left", underline=0,
                               command=main_window.import_rooms_command)

        self.rooms.add_command(label="Uložit místnosti",
                               image=main_window.icons.file_save_icon,
                               compound="left", underline=0,
                               command=main_window.export_rooms_command)

        self.rooms.add_command(label="Uložit místnosti jiným jménem",
                               image=main_window.icons.file_save_as_icon,
                               compound="left", underline=1,
                               command=main_window.export_rooms_as_command)

        self.rooms.add_separator()

        self.rooms.add_command(label="Seznam místností ze SAPu",
                               image=main_window.icons.rooms_from_sap,
                               compound="left", underline=1,
                               command=main_window.import_rooms_from_sap)

        self.rooms.add_command(label="Synchronizace místností ze SAPem",
                               image=main_window.icons.reload_icon,
                               compound="left", underline=1,
                               command=main_window.synchronize_rooms_with_sap)

        self.edit = tkinter.Menu(self, tearoff=0)
        self.edit.add_command(label="Nakreslit místnost",
                              image=main_window.icons.edit_icon,
                              compound="left", underline=0,
                              command=self.main_window.draw_new_room_command)
        # accelerator="Ctrl+N")

        self.edit.add_command(label="Vybrat polygon pro místnost",
                              image=main_window.icons.rectangle,
                              compound="left", underline=0,
                              command=self.main_window.draw_new_room_command)
        # accelerator="Ctrl+P")

        self.view = tkinter.Menu(self, tearoff=0)
        self.view.add_command(label="Zvětšit",
                              image=main_window.icons.zoom_in_icon,
                              compound="left", underline=1, accelerator="Ctrl++",
                              command=main_window.zoom_plus)
        self.view.add_command(label="Zmenšit",
                              image=main_window.icons.zoom_out_icon,
                              compound="left", underline=1, accelerator="Ctrl+-",
                              command=main_window.zoom_minus)
        self.view.add_command(label="1:1",
                              image=main_window.icons.zoom_original_icon,
                              compound="left", underline=0, accelerator="Ctrl+0",
                              command=main_window.redraw)
        self.view.add_separator()
        self.view.add_command(label="Mřížka",
                              image=main_window.icons.view_grid_icon,
                              compound="left", underline=0,
                              command=canvas.toggle_grid)
        self.view.add_command(label="Okraj výkresu",
                              image=main_window.icons.view_boundary_icon,
                              compound="left", underline=0,
                              command=canvas.toggle_boundary)

        self.tools = tkinter.Menu(self, tearoff=0)

        self.tools.add_command(label="Informace o výkresu",
                               image=main_window.icons.drawing_info_icon,
                               compound="left", underline=0,
                               command=self.show_drawing_info_dialog,
                               accelerator="Ctrl+I")

        self.tools.add_separator()
        # self.tools.add_command(label="Nastavení",
        #                        image=main_window.icons.properties_icon,
        #                        compound="left", underline=0,
        #                        command=self.show_settings_dialog)
        # self.tools.add_separator()
        self.tools.add_command(label="Zkontrolovat připojení k serveru",
                               image=main_window.icons.checkbox_icon,
                               compound="left", underline=0,
                               command=self.check_server_connectivity)
        self.tools.add_command(label="Verze rozhraní serveru",
                               image=main_window.icons.service_icon,
                               compound="left", underline=0,
                               command=self.check_service_version)

        self.helpmenu = tkinter.Menu(self, tearoff=0)
        self.helpmenu.add_command(label="Nápověda",
                                  image=main_window.icons.help_faq_icon,
                                  compound="left", underline=0, accelerator="F1",
                                  command=help)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="O programu",
                                  image=main_window.icons.help_about_icon, accelerator="F11",
                                  compound="left", underline=0, command=about)
        self.helpmenu.add_command(label="Aktuální konfigurace",
                                  image=main_window.icons.configure, accelerator="F12",
                                  compound="left", underline=0,
                                  command=lambda: configure(self.main_window.configuration))

        self.add_cascade(label="Soubor", menu=self.filemenu, underline=0)
        self.add_cascade(label="Upravit", menu=self.edit, underline=0)
        self.add_cascade(label="Místnosti", menu=self.rooms, underline=0)
        self.add_cascade(label="Zobrazit", menu=self.view, underline=0)
        self.add_cascade(label="Nástroje", menu=self.tools, underline=3)
        self.add_cascade(label="Nápověda", menu=self.helpmenu, underline=0)

        self.parent.bind("<F1>", lambda event: help())
        self.parent.bind("<F11>", lambda event: about())
        self.parent.bind("<F12>", lambda event: configure(self.main_window.configuration))
        self.parent.bind("<Control-q>", lambda event: parent.quit())
        self.parent.bind("<Control-n>", lambda event: main_window.draw_new_room_command())
        self.parent.bind("<Control-i>", lambda event: self.show_drawing_info_dialog())
        self.parent.bind("<Control-m>", lambda event: self.show_room_list_dialog())
        self.parent.bind("<Control-0>", lambda event: main_window.redraw())

    def show_settings_dialog(self):
        """Show settings dialog."""
        SettingsDialog(self.parent)

    def show_drawing_info_dialog(self):
        """Show drawing info dialog."""
        DrawingInfoDialog(self.parent, self.main_window.drawing)

    def show_room_list_dialog(self):
        """Show room list dialog."""
        RoomListDialog(self.parent, self.main_window.drawing)

    def check_server_connectivity(self):
        """Check the connectivity to server and display results."""
        address = self.main_window.configuration.server_address
        port = self.main_window.configuration.server_port
        if not address:
            messagebox.showerror("Nastala chyba", "Není nastavená adresa serveru")
            return
        if not port:
            messagebox.showerror("Nastala chyba", "Není nastaven port serveru")
            return
        url = DrawServiceInterface.get_url(address, port)
        drawServiceInterface = DrawServiceInterface(service_url=url)
        status, message = drawServiceInterface.check_liveness()
        if status:
            messagebox.showinfo("Připojení k serveru", "Připojení k serveru: Ok")
        else:
            messagebox.showerror("Nastala chyba", "Nastala chyba: {e}".format(e=message))

    def check_service_version(self):
        """Check the version of web service and display results."""
        address = self.main_window.configuration.server_address
        port = self.main_window.configuration.server_port
        if not address:
            messagebox.showerror("Nastala chyba", "Není nastavená adresa serveru")
            return
        if not port:
            messagebox.showerror("Nastala chyba", "Není nastaven port serveru")
            return
        url = DrawServiceInterface.get_url(address, port)
        drawServiceInterface = DrawServiceInterface(service_url=url)
        status, version, message = drawServiceInterface.read_version()
        if status:
            messagebox.showinfo("Verze rozhraní", "Verze rozhraní: {v}".format(v=version))
        else:
            messagebox.showerror("Nastala chyba", "Nastala chyba: {e}".format(e=message))

    def disable_ui_items_for_no_drawing_mode(self):
        """Disable UI (menu) items when the application is set to no drawing mode."""
        Menubar.disable_menu_item(self.filemenu, 1)
        Menubar.disable_menu_item(self.filemenu, 3)

        Menubar.disable_menu_item(self.rooms, 0)
        Menubar.disable_menu_item(self.rooms, 2)
        Menubar.disable_menu_item(self.rooms, 3)
        Menubar.disable_menu_item(self.rooms, 4)
        Menubar.disable_menu_item(self.rooms, 6)
        Menubar.disable_menu_item(self.rooms, 7)

        Menubar.disable_menu_item(self.edit, 0)
        Menubar.disable_menu_item(self.edit, 1)

        Menubar.disable_menu_item(self.view, 0)
        Menubar.disable_menu_item(self.view, 1)
        Menubar.disable_menu_item(self.view, 2)
        Menubar.disable_menu_item(self.view, 4)
        Menubar.disable_menu_item(self.view, 5)

        Menubar.disable_menu_item(self.tools, 0)
        # Menubar.disable_menu_item(self.tools, 1)

    def enable_ui_items_for_drawing_mode(self):
        """Enable UI (menu) items when the application is set to no drawing mode."""
        Menubar.enable_menu_item(self.filemenu, 1)
        Menubar.enable_menu_item(self.filemenu, 3)

        Menubar.enable_menu_item(self.rooms, 0)
        Menubar.enable_menu_item(self.rooms, 2)
        Menubar.enable_menu_item(self.rooms, 3)
        Menubar.enable_menu_item(self.rooms, 4)
        Menubar.enable_menu_item(self.rooms, 6)
        Menubar.enable_menu_item(self.rooms, 7)

        Menubar.enable_menu_item(self.edit, 0)
        Menubar.enable_menu_item(self.edit, 1)

        Menubar.enable_menu_item(self.view, 0)
        Menubar.enable_menu_item(self.view, 1)
        Menubar.enable_menu_item(self.view, 2)
        Menubar.enable_menu_item(self.view, 4)
        Menubar.enable_menu_item(self.view, 5)

        Menubar.enable_menu_item(self.tools, 0)
        # Menubar.enable_menu_item(self.tools, 1)

    @staticmethod
    def disable_menu_item(menu, index):
        """Disable specified menu item."""
        menu.entryconfig(index, state="disabled")

    @staticmethod
    def enable_menu_item(menu, index):
        """Enable specified menu item."""
        menu.entryconfig(index, state="normal")
