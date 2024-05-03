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

from configuration import Configuration


def configure(configuration: Configuration):
    """Show configuration dialog."""
    msg = f"Typ aplikace: {configuration.app_type}\n\nAdresa serveru: {configuration.server_address}\nPort serveru: {configuration.server_port}"
    messagebox.showinfo("Aktuální konfigurace", msg)
