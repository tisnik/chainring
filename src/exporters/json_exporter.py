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

"""Drawing exporter to JSON."""

from datetime import *
import json

from drawing import Drawing
from geometry.bounds import Bounds
from geometry.rescaler import Rescaler


class JSONExporter:
    """Drawing exporter to JSON."""

    VERSION = 1
    SCALES = [
        [320, 240],
        [400, 300],
        [640, 480],
        [800, 600],
        [1024, 768]
    ]

    def __init__(self, filename, drawing):
        """Initialize the exporter, set the filename to be created and a sequence of entities."""
        self.filename = filename
        self.entities = drawing.entities
        self.rooms = drawing.rooms

    @staticmethod
    def get_timestamp():
        """Get the timestamp for the current time and format it according to ISO."""
        return datetime.now().isoformat(sep=' ')

    @staticmethod
    def write_room(fout, room):
        """Write the room data into the generated file."""
        vertexes = room["polygon"]
        fout.write("R {id} {vertex_count}".format(id=room["room_id"],
                                                  vertex_count=len(vertexes)))
        for vertex in vertexes:
            fout.write(" {x} {y}".format(x=vertex[0], y=vertex[1]))
        fout.write("\n")

    def export(self):
        """Export the whole drawing into the JSON file."""

        bounds = Bounds.computeBounds(self.entities)
        scales = []

        for scale in JSONExporter.SCALES:
            xoffset, yoffset, s = Rescaler.computeScale(bounds, scale[0], scale[1])
            scales.append({"width": scale[0],
                           "height": scale[1],
                           "xoffset": xoffset,
                           "yoffset": yoffset,
                           "scale": s})

        entities_list = []
        for entity in self.entities:
            entities_list.append(entity.asDict())

        obj = {
            "created": self.get_timestamp(),
            "version": JSONExporter.VERSION,
            "bounds": bounds.__dict__,
            "scales": scales,
            "entities_count": len(self.entities),
            "rooms_count": len(self.rooms),
            "entities": entities_list,
        }
        with open(self.filename, "w") as fout:
            json.dump(obj, fout, indent="\t")

#           for room in self.rooms:
#               DrawingExporter.write_room(fout, room)