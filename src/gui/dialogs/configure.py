"""Implementation of simple 'Configure' dialog."""

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


def configure(configuration):
    """Show configuration dialog."""
    msg = "Typ aplikace: {t}\n\nAdresa serveru: {a}\nPort serveru: {p}".format(
        t=configuration.app_type,
        a=configuration.server_address,
        p=configuration.server_port)
    messagebox.showinfo("Aktuální konfigurace",
                        msg)
