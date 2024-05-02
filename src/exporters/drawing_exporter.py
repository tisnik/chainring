"""Drawing exporter (serializer) to structured text format."""

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

from geometry.bounds import Bounds
from geometry.rescaler import Rescaler
from drawing import Drawing
from io import TextIOWrapper
from typing import Optional, Union


class DrawingExporter:
    """Drawing exporter (serializer) to structured text format."""

    # supported versions:
    # 1 - supports line, circle, arc, text, w/o color, w/o layer
    # 2 - supports v1 + polyline + color + layer

    # the default version
    VERSION = 2

    # supported scales to be used in drawing files
    SCALES = [
        [320, 240],
        [400, 300],
        [640, 480],
        [800, 600],
        [1024, 768],
    ]

    def __init__(self, filename: str, drawing: Drawing) -> None:
        """Initialize the exporter, set the filename to be created and a sequence of entities."""
        self.filename = filename
        self.entities = drawing.entities
        self.rooms = drawing.rooms
        self.drawing_id = drawing.drawing_id

    @staticmethod
    def get_timestamp() -> str:
        """Get the timestamp for the current time and format it according to ISO."""
        return datetime.now().isoformat(sep=" ")

    @staticmethod
    def output_timestamp(fout: TextIOWrapper) -> None:
        """Write the timestamp into the generated file."""
        fout.write(f"created: {DrawingExporter.get_timestamp()}\n")

    @staticmethod
    def output_version(fout: TextIOWrapper) -> None:
        """Write the version into the generated file."""
        fout.write(f"version: {DrawingExporter.VERSION}\n")

    @staticmethod
    def output_drawing_id(fout, drawing_id):
        """Write the ID into the generated file."""
        fout.write(f"id: {drawing_id}\n")

    @staticmethod
    def write_room(
        fout: TextIOWrapper,
        room: dict[str, str | list[tuple[float, float]] | int | None],
    ) -> None:
        """Write the room data into the generated file."""
        vertexes = room["polygon"]
        # export only room with polygon
        if vertexes is not None:
            fout.write(
                "R {id} {vertex_count}".format(
                    id=room["room_id"], vertex_count=len(vertexes)
                )
            )
            for vertex in vertexes:
                fout.write(f" {vertex[0]} {vertex[1]}")
        # room without polygon need to have zero vertexes
        else:
            fout.write("R {id} 0".format(id=room["room_id"]))

        # the room type field is optional
        if "type" in room:
            fout.write(" {t}".format(t=room["type"]))

        fout.write("\n")

    # TODO: refactor this function
    def export(self) -> None:
        """Export (serialize) the whole drawing into the text file."""
        with open(self.filename, "w") as fout:
            DrawingExporter.output_version(fout)

            # write drawing ID, but only when the ID is known/specified
            if self.drawing_id is not None:
                DrawingExporter.output_drawing_id(fout, self.drawing_id)

            DrawingExporter.output_timestamp(fout)

            # compute drawing bounds and write them into the file
            bounds = Bounds.compute_bounds(self.entities)
            fout.write(f"bounds: {bounds}\n")

            # compute drawing scales and write them into the file
            for scale in DrawingExporter.SCALES:
                xoffset, yoffset, s = Rescaler.compute_scale(bounds, scale[0], scale[1])
                fout.write(f"scale: {scale[0]} {scale[1]} {s}\n")

            fout.write(f"entities: {len(self.entities)}\n")
            fout.write(f"rooms: {len(self.rooms)}\n")

            # write all entities
            for entity in self.entities:
                fout.write(entity.str())
                fout.write("\n")

            # write all rooms
            for room in self.rooms:
                DrawingExporter.write_room(fout, room)
