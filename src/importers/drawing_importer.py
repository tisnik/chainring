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

"""Importer for drawings stored in a text file."""

import sys

from drawing import Drawing
from entities.drawing_entity_type import *
from entities.line import *
from entities.circle import *
from entities.arc import *
from entities.text import *


class DrawingImporter:
    """Importer for drawings stored in a text file."""

    def __init__(self, filename):
        """Initialize the object, set the filename to be read, and setup callback functions."""
        self.filename = filename

        self.commands = {
            "version:": DrawingImporter.process_version,
            "created:": DrawingImporter.process_created,
            "entities:": DrawingImporter.process_entities,
            "rooms:": DrawingImporter.process_rooms,
            "bounds:": DrawingImporter.process_bounds,
            "scale:": DrawingImporter.process_scale,
            "L": DrawingImporter.process_line,
            "C": DrawingImporter.process_circle,
            "A": DrawingImporter.process_arc,
            "T": DrawingImporter.process_text,
            "R": DrawingImporter.process_room,
        }

        self.statistic = {
            DrawingEntityType.LINE: 0,
            DrawingEntityType.CIRCLE: 0,
            DrawingEntityType.ARC: 0,
            DrawingEntityType.TEXT: 0,
        }
        self.metadata = {}
        self.entities = []
        self.rooms = []

    def import_drawing(self):
        """Import the file and return structure containing all entities."""
        with open(self.filename) as fin:
            lines = 0
            for line in fin:
                self.parse_line(line)
                lines += 1
        drawing = Drawing(self.entities, self.statistic, lines)
        drawing.rooms = self.rooms
        # TODO this needs to be improved for deleted rooms
        drawing.room_counter = len(self.rooms) + 1
        return drawing

    def parse_line(self, line):
        """Parse one line in the input file."""
        parts = line.split(" ")
        # remove end of lines
        parts = [item.strip() for item in parts]
        command = parts[0]
        function = self.commands.get(command,
                                     DrawingImporter.process_unknown_command)
        function(self, parts)

    def process_unknown_command(self, parts):
        """Pprocess unknown command(s)."""
        print("Unknown command: '{c}'".format(c=parts[0]))
        sys.exit(0)

    def process_version(self, parts):
        """Process drawing version."""
        version = parts[1].strip()
        print("Read attribute 'version': {v}".format(v=version))
        self.metadata["version"] = version

    def process_created(self, parts):
        """Process the date when drawing was created."""
        created = " ".join(parts[1:]).strip()
        print("Read attribute 'created': {c}".format(c=created))
        self.metadata["created"] = created

    def process_entities(self, parts):
        """Process number of entities."""
        entities = parts[1].strip()
        print("Read attribute 'entities': {e}".format(e=entities))
        self.metadata["entities"] = entities

    def process_rooms(self, parts):
        """Process number of rooms."""
        rooms = parts[1].strip()
        print("Read attribute 'rooms': {r}".format(r=rooms))
        self.metadata["rooms"] = rooms

    def process_bounds(self, parts):
        """Process the bounds line."""
        # we don't need this attribute ATM
        pass

    def process_scale(self, parts):
        """Process the scale line."""
        # we don't need this attribute ATM
        pass

    def process_line(self, parts):
        """Process line entity."""
        x1 = float(parts[1])
        y1 = float(parts[2])
        x2 = float(parts[3])
        y2 = float(parts[4])
        self.statistic[DrawingEntityType.LINE] += 1
        self.entities.append(Line(x1, y1, x2, y2))

    def process_circle(self, parts):
        """Process circle entity."""
        x = float(parts[1])
        y = float(parts[2])
        radius = float(parts[3])
        self.statistic[DrawingEntityType.CIRCLE] += 1
        self.entities.append(Circle(x, y, radius))

    def process_arc(self, parts):
        """Process arc entity."""
        x = float(parts[1])
        y = float(parts[2])
        radius = float(parts[3])
        angle1 = float(parts[4])
        angle2 = float(parts[5])
        self.statistic[DrawingEntityType.ARC] += 1
        self.entities.append(Arc(x, y, radius, angle1, angle2))

    def process_text(self, parts):
        """Process text entity."""
        x = float(parts[1])
        y = float(parts[2])
        text = " ".join(parts[3:]).strip()
        self.statistic[DrawingEntityType.TEXT] += 1
        self.entities.append(Text(x, y, text))

    def process_room(self, parts):
        """Process room polygon."""
        room_id = parts[1]
        vertexes = int(parts[2])
        coordinates = parts[3:]
        polygon = list((float(coordinates[i*2]), float(coordinates[i*2+1])) for i in range(vertexes))
        self.rooms.append({"room_id": room_id,
                           "polygon": polygon})
