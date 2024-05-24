"""Importer (deserializer) for drawings stored in a binary format."""

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


class BinaryImporter:
    """Importer (deserializer) for drawings stored in a binary format."""

    def __init__(self, filename) -> None:
        """Initialize the importer for drawings stored in binary format."""
        self.filename = filename

    def import_binary_drawing(self):
        """Import the binary file and return structure with all entities."""
        with open(self.filename, "rb") as fin:
            return pickle.load(fin)
