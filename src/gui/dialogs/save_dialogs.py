"""Dialogs used to save drawings and rooms."""

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
from tkinter import filedialog


class SaveDialogs:
    """Dialogs used to save drawings and rooms."""

    @staticmethod
    def save_drawing(root):
        """Display dialog to save drawing."""
        filetypes = [('Výkresy', '*.drw')]
        dialog = filedialog.SaveAs(root, filetypes=filetypes)
        return dialog.show()

    @staticmethod
    def save_rooms(root):
        """Display dialog to save rooms."""
        filetypes = [('Místnosti', '*.rooms')]
        dialog = filedialog.SaveAs(root, filetypes=filetypes)
        return dialog.show()

    @staticmethod
    def save_rooms_as_csv(root):
        """Display dialog to save rooms into the CSV file."""
        filetypes = [('Soubory CSV', '*.csv')]
        dialog = filedialog.SaveAs(root, filetypes=filetypes)
        return dialog.show()

    @staticmethod
    def save_rooms_as_txt(root):
        """Display dialog to save rooms into the txt file."""
        filetypes = [('Textové soubory', '*.txt')]
        dialog = filedialog.SaveAs(root, filetypes=filetypes)
        return dialog.show()
