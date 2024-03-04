"""Importer (deserializer) for drawings stored in structured text file."""

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

import sys

from drawing import Drawing
from entities.drawing_entity_type import DrawingEntityType
from entities.line import Line
from entities.circle import Circle
from entities.arc import Arc
from entities.text import Text
from entities.polyline import Polyline


class DrawingImporter:
    """Importer (deserializer) for drawings stored in structured text file."""

    def __init__(self, filename):
        """Initialize the object, set the filename to be read, and setup callback functions."""
        self.filename = filename

        self.commands = {
            "version:": DrawingImporter.process_version,
            "id:": DrawingImporter.process_id,
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
            "P": DrawingImporter.process_polyline
        }

        self.statistic = {
            DrawingEntityType.LINE: 0,
            DrawingEntityType.CIRCLE: 0,
            DrawingEntityType.ARC: 0,
            DrawingEntityType.TEXT: 0,
            DrawingEntityType.POLYLINE: 0,
        }
        self.metadata = {}
        self.entities = []
        self.rooms = []
        self.drawing_id = None

    def import_drawing(self):
        """Import the file and return structure containing all entities."""
        try:
            # read and parse all lines
            with open(self.filename) as fin:
                lines = 0
                for line in fin:
                    self.parse_line(line)
                    lines += 1
            drawing = Drawing(self.entities, self.statistic, lines)
            drawing.rooms = self.rooms
            drawing.drawing_id = self.drawing_id
            # TODO this needs to be improved for deleted rooms
            drawing.room_counter = len(self.rooms) + 1
            return drawing
        except Exception as e:
            print(e)
            return None

    def parse_line(self, line):
        """Parse one line in the input file."""
        parts = line.split(" ")
        # remove end of lines
        parts = [item.strip() for item in parts]
        # first string or word is a command
        command = parts[0]
        function = self.commands.get(command,
                                     DrawingImporter.process_unknown_command)
        function(self, parts)

    def process_unknown_command(self, parts):
        """Pprocess unknown command(s)."""
        print("Unknown command: '{c}'".format(c=parts[0]))
        sys.exit(0)

    def process_id(self, parts):
        """Process command with drawing ID."""
        drawing_id = parts[1].strip()
        print("Read attribute 'id': {id}".format(id=drawing_id))
        self.drawing_id = drawing_id

    def process_version(self, parts):
        """Process command with drawing version."""
        version = parts[1].strip()
        print("Read attribute 'version': {v}".format(v=version))
        self.metadata["version"] = version

    def process_created(self, parts):
        """Process command with the date when drawing was created."""
        created = " ".join(parts[1:]).strip()
        print("Read attribute 'created': {c}".format(c=created))
        self.metadata["created"] = created

    def process_entities(self, parts):
        """Process command with number of entities."""
        entities = parts[1].strip()
        print("Read attribute 'entities': {e}".format(e=entities))
        self.metadata["entities"] = entities

    def process_rooms(self, parts):
        """Process command with number of rooms."""
        rooms = parts[1].strip()
        print("Read attribute 'rooms': {r}".format(r=rooms))
        self.metadata["rooms"] = rooms

    def process_bounds(self, parts):
        """Process command with the bounds line."""
        # we don't need this attribute ATM
        pass

    def process_scale(self, parts):
        """Process command with the scale line."""
        # we don't need this attribute ATM
        pass

    def process_line(self, parts):
        """Process command with line entity."""
        try:
            color = int(parts[1])
        except Exception as e:
            color = 0
        layer = parts[2]
        x1 = float(parts[3])
        y1 = float(parts[4])
        x2 = float(parts[5])
        y2 = float(parts[6])
        self.statistic[DrawingEntityType.LINE] += 1
        self.entities.append(Line(x1, y1, x2, y2, color, layer))

    def process_circle(self, parts):
        """Process command with circle entity."""
        try:
            color = int(parts[1])
        except:
            color = 0
        layer = parts[2]
        x = float(parts[3])
        y = float(parts[4])
        radius = float(parts[5])
        self.statistic[DrawingEntityType.CIRCLE] += 1
        self.entities.append(Circle(x, y, radius, color, layer))

    def process_arc(self, parts):
        """Process command with arc entity."""
        try:
            color = int(parts[1])
        except:
            color = 0
        layer = parts[2]
        x = float(parts[3])
        y = float(parts[4])
        radius = float(parts[5])
        angle1 = float(parts[6])
        angle2 = float(parts[7])
        self.statistic[DrawingEntityType.ARC] += 1
        self.entities.append(Arc(x, y, radius, angle1, angle2, color, layer))

    def process_text(self, parts):
        """Process command with text entity."""
        try:
            color = int(parts[1])
        except:
            color = 0
        layer = parts[2]
        x = float(parts[3])
        y = float(parts[4])
        text = " ".join(parts[5:]).strip()
        text = text.replace("^2^", u"\u00B2")
        self.statistic[DrawingEntityType.TEXT] += 1
        self.entities.append(Text(x, y, text, color, layer))

    def process_polyline(self, parts):
        """Process command with polyline entity."""
        try:
            color = int(parts[1])
        except:
            color = 0
        layer = parts[2]
        vertexes = int(parts[3])
        coordinates = parts[4:]
        # first half of coordinates
        xpoints = list(float(i) for i in coordinates[:vertexes])
        # second half of coordinates
        ypoints = list(float(i) for i in coordinates[vertexes:])
        self.statistic[DrawingEntityType.POLYLINE] += 1
        self.entities.append(Polyline(xpoints, ypoints, color, layer))

    def process_room(self, parts):
        """Process command with room polygon."""
        room_id = parts[1]
        vertexes = int(parts[2])
        coordinates = parts[3:]
        polygon = list((float(coordinates[i * 2]), float(coordinates[i * 2 + 1]))
                       for i in range(vertexes))
        last_part = parts[-1]
        # type: drawn from polygon or from series of line vertexes
        if last_part == "P" or last_part == "L":
            typ = last_part
        else:
            typ = "?"
        self.rooms.append({"room_id": room_id,
                           "polygon": polygon,
                           "type": typ})
