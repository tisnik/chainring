"""Drawing exporter (serializer) to DXF format."""

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


class DXFExporter:
    """Drawing exporter (serializer) to DXF format."""

    def __init__(self, filename, entities):
        """Initialize the exporter, set the filename to be created and a sequence of entities."""
        self.filename = filename
        self.entities = entities

    def export(self):
        """Perform the serialiation of drawing into DXF format."""
        # TODO: implement this feature
        #  with open(self.filename, "w") as fout:
