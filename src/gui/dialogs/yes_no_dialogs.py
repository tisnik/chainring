"""Simple yes/no dialogs implementations."""

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

from tkinter import messagebox


def dialog_store_vertex_with_three_vertexes():
    """Show dialog with the question whether to draw room with three vertexes."""
    return messagebox.askyesno("Místnost jen se třemi rohy",
                               "Opravdu si přejete nakreslit místnost jen se třemi rohy?")


def dialog_delete_whole_room(sap_id):
    """Show dialog with the question whether to delete whole room."""
    message = "Opravdu si přejete smazat celou místnost s označením " + sap_id + "?"
    return messagebox.askyesno("Smazat místnost", message)


def dialog_delete_room_polygon(sap_id):
    """Show dialog with the question whether to delete room polygon."""
    message = "Opravdu si přejete smazat obrys místnosti s označením " + sap_id + "?"
    return messagebox.askyesno("Smazat obrys mísnosti", message)


def dialog_load_new_drawing():
    """Show dialog with the question whether to delete current drawing and load new one from file.""" # noqa: E501
    message = "Opravdu si přejete smazat stávající výkres a načíst výkres nový?"
    return messagebox.askyesno("Smazat stávající výkres", message)


def dialog_load_rooms():
    """Show dialog with the question whether to delete current rooms and load new ones."""
    message = "Opravdu si přejete smazat stávající místnosti a načíst místnosti ze souboru?"
    return messagebox.askyesno("Smazat stávající mísnosti", message)


def dialog_load_rooms_from_sap():
    """Show dialog with the question whether to delete current rooms and load new ones from SAP."""
    message = "Opravdu si přejete smazat stávající místnosti a načíst místnosti ze SAPu?"
    return messagebox.askyesno("Smazat stávající mísnosti", message)


def dialog_synchronize_rooms_with_sap():
    """Show dialog with the question whether to synchronize with SAP."""
    message = "Opravdu si přejete synchronizovat stávající místnosti ze SAPem?"
    return messagebox.askyesno("Synchronizace se SAPem", message)
