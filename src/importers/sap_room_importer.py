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


class SapRoomImporter:
    """Importer for rooms stored in a text file."""

    def __init__(self, filename) -> None:
        """Initialize the object, set the filename to be read, and setup callback functions."""
        self.filename = filename

        self.commands = {
            "version:": SapRoomImporter.process_version,
            "created:": SapRoomImporter.process_created,
            "rooms:": SapRoomImporter.process_rooms,
            "R": SapRoomImporter.process_room,
        }

        self.metadata = {}
        self.rooms = []

    def import_rooms(self):
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

    def parse_line(self, line) -> None:
        """Parse one line in the input file."""
        parts = line.split(" ")
        # remove end of lines
        parts = [item.strip() for item in parts]
        command = parts[0]
        function = self.commands.get(
            command, SapRoomImporter.process_room_without_prefix
        )
        function(self, parts)

    def process_unknown_command(self, parts) -> None:
        """Process unknown command(s)."""
        print(f"Unknown command: '{parts[0]}'")
        sys.exit(0)

    def process_version(self, parts) -> None:
        """Process data file version."""
        version = parts[1].strip()
        print(f"Read attribute 'version': {version}")
        self.metadata["version"] = version

    def process_created(self, parts) -> None:
        """Process the date when data file was created."""
        created = " ".join(parts[1:]).strip()
        print(f"Read attribute 'created': {created}")
        self.metadata["created"] = created

    def process_rooms(self, parts) -> None:
        """Process number of rooms."""
        rooms = parts[1].strip()
        print(f"Read attribute 'rooms': {rooms}")
        self.metadata["rooms"] = rooms

    def process_room(self, parts) -> None:
        """Process room polygon."""
        room_id = parts[1]
        polygon = []
        self.rooms.append({"room_id": room_id, "polygon": polygon})

    def process_room_without_prefix(self, parts) -> None:
        """Process room polygon."""
        room_id = parts[0]
        polygon = []
        self.rooms.append({"room_id": room_id, "polygon": polygon})
