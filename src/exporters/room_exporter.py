"""Rooms exporter (serializer) to structured text format."""

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

from datetime import datetime
from io import TextIOWrapper

from drawing import Drawing


class RoomExporter:
    """Rooms exporter (serializer) to structured text format."""

    # currently supported version
    VERSION = 1

    def __init__(self, filename: str, drawing: Drawing) -> None:
        """Initialize the exporter, set the filename to be created and a sequence of entities."""
        self.filename = filename
        self.rooms = drawing.rooms

    @staticmethod
    def get_timestamp() -> str:
        """Get the timestamp for the current time and format it according to ISO."""
        return datetime.now().isoformat(sep=" ")

    @staticmethod
    def output_timestamp(fout: TextIOWrapper) -> None:
        """Write the timestamp into the generated file."""
        fout.write(f"created: {RoomExporter.get_timestamp()}\n")

    @staticmethod
    def output_version(fout: TextIOWrapper) -> None:
        """Write the version into the generated file."""
        fout.write(f"version: {RoomExporter.VERSION}\n")

    @staticmethod
    def write_room(
        fout: TextIOWrapper,
        room: dict[str, str | list[tuple[float, float]] | int | None],
    ) -> None:
        """Write the room data into the generated file."""
        vertexes = room["polygon"]
        # export only room with polygon
        if vertexes is not None and type(vertexes) is list:
            fout.write(
                "R {id} {vertex_count}".format(
                    id=room["room_id"], vertex_count=len(vertexes)
                )
            )
            for vertex in vertexes:
                fout.write(f" {vertex[0]} {vertex[1]}")
        # room without polygon needs to have zero vertexes specified
        else:
            fout.write("R {id} 0".format(id=room["room_id"]))

        if "type" in room:
            fout.write(" {t}".format(t=room["type"]))

        fout.write("\n")

    def export(self) -> None:
        """Export (serialize) room list into the text file."""
        with open(self.filename, "w") as fout:
            # metadata
            RoomExporter.output_version(fout)
            RoomExporter.output_timestamp(fout)

            # number of rooms
            fout.write(f"rooms: {len(self.rooms)}\n")
            # export all rooms
            for room in self.rooms:
                RoomExporter.write_room(fout, room)
