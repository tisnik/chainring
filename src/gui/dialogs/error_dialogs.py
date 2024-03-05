"""Various errors dialogs."""

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


def error_dialog_drawing_load():
    """Show dialog when drawing import was not successful."""
    messagebox.showerror("Chyba při načítání výkresu",
                         "Při načítání výkresu došlo k neočekávané chybě")


def error_dialog_wrong_configuration(message):
    """Show dialog when configuration is not proper."""
    messagebox.showerror("Chyba konfigurace aplikace", message)
