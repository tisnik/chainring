"""Importer for rooms stored in a text file."""

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
from typing import Optional


class RoomImporter:
    """Importer for rooms stored in a text file."""

    def __init__(self, filename: str) -> None:
        """Initialize the object, set the filename to be read, and setup callback functions."""
        self.filename = filename

        self.commands = {
            "version:": RoomImporter.process_version,
            "created:": RoomImporter.process_created,
            "rooms:": RoomImporter.process_rooms,
            "R": RoomImporter.process_room,
        }

        self.metadata : dict[str, str] = {}
        self.rooms : list = []

    def import_rooms(self) -> Optional[list[dict[str, str]]]:
        """Import the file and return structure containing all entities."""
        try:
            with open(self.filename) as fin:
                lines = 0
                for line in fin:
                    self.parse_line(line)
                    lines += 1
            return self.rooms
        except Exception as e:
            return None

    def parse_line(self, line: str) -> None:
        """Parse one line in the input file."""
        parts = line.split(" ")
        # remove end of lines
        parts = [item.strip() for item in parts]
        command = parts[0]
        function = self.commands.get(command, RoomImporter.process_unknown_command)
        function(self, parts)

    def process_unknown_command(self, parts: list[str]) -> None:
        """Process unknown command(s)."""
        print(f"Unknown command: '{parts[0]}'")
        sys.exit(0)

    def process_version(self, parts: list[str]) -> None:
        """Process data file version."""
        version = parts[1].strip()
        print(f"Read attribute 'version': {version}")
        self.metadata["version"] = version

    def process_created(self, parts: list[str]) -> None:
        """Process the date when data file was created."""
        created = " ".join(parts[1:]).strip()
        print(f"Read attribute 'created': {created}")
        self.metadata["created"] = created

    def process_rooms(self, parts: list[str]) -> None:
        """Process number of rooms."""
        rooms = parts[1].strip()
        print(f"Read attribute 'rooms': {rooms}")
        self.metadata["rooms"] = rooms

    def process_room(self, parts: list[str]) -> None:
        """Process room polygon."""
        room_id = parts[1]
        vertexes = int(parts[2])
        coordinates = parts[3:]
        polygon = list(
            (float(coordinates[i * 2]), float(coordinates[i * 2 + 1]))
            for i in range(vertexes)
        )
        last_part = parts[-1]
        if last_part == "P" or last_part == "L":
            typ = last_part
        else:
            typ = "?"
        self.rooms.append({"room_id": room_id, "polygon": polygon, "type": typ})
