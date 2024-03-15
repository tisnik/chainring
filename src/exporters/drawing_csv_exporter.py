"""Drawing exporter (serializer) to CVS."""

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


class CSVExporter:
    """Drawing exporter (serializer) to CVS."""

    def __init__(self, filename, entities):
        """Initialize the exporter (serializer), set the filename to be created and a sequence of entities."""
        self.filename = filename
        self.entities = entities

    def export(self):
        """Perform the export."""
        # TODO: implement this feature
