"""Module to export (serialize) whole drawing into a binary file."""

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

import pickle


class BinaryExporter:
    """Class to export (serialize) whole drawing into a binary file."""

    def __init__(self, filename, entities):
        """Initialize the exporter."""
        self.filename = filename
        self.entities = entities

    def export_binary_drawing(self) -> None:
        """Export (serialize) the drawing into a binary file."""
        with open(self.filename, "wb") as fout:
            # at this moment we use simple approach:
            # dump() function from pickle module
            pickle.dump(self.entities, fout)
