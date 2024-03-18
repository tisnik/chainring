"""Implementation of simple 'About' dialog."""

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

from tkinter import messagebox


def about():
    """Show 'about' dialog."""
    messagebox.showinfo(
        "O programu",
        "Integrace CAD výkresů do SAP\n(c) 2017, 2018 eLevel system s.r.o.",
    )
