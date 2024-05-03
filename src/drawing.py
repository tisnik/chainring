"""Representation of vector drawing."""


from typing import Optional

from entities.arc import Arc
from entities.circle import Circle
from entities.drawing_entity_type import DrawingEntityType
from entities.line import Entity
from entities.line import Line
from entities.polyline import Polyline
from entities.text import Text

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


class Drawing:
    """Representation of vector drawing."""

    def __init__(
        self,
        entities: list[Line | Arc | Circle | Text | Polyline],
        statistic: dict[DrawingEntityType, int],
        lines: int = 0,
        metadata: None = None,
    ) -> None:
        """Initialize the class, setup entities."""
        self._entities = entities
        self._drawing_id = None
        self._statistic = statistic
        self._lines = lines
        self._rooms = []
        self._metadata = metadata or {}
        self._room_counter = 1
        self._filename = None

    @property
    def entities(self):
        """Property holding all entities on drawing."""
        return self._entities

    @entities.setter
    def entities(self, entities):
        """Setter for property holding all entities on drawing."""
        self._entities = entities

    @property
    def room_counter(self):
        """Property holding room counter."""
        return self._room_counter

    @entities.setter
    def room_counter(self, new_value):
        """Setter for property holding room counter."""
        self._room_counter = new_value

    @property
    def statistic(self):
        """Property holding drawing statistic."""
        return self._statistic

    @statistic.setter
    def statistic(self, statistic):
        """Setter for property holding drawing statistic."""
        self._statistic = statistic

    @property
    def lines(self):
        """Input lines."""
        return self._lines

    @lines.setter
    def lines(self, lines):
        """Setter for input lines."""
        self._lines = lines

    @property
    def metadata(self):
        """Drawing metadata."""
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Setter for drawing metadata."""
        self._metadata = metadata

    @property
    def rooms(self):
        """Rooms on drawing."""
        return self._rooms

    @rooms.setter
    def rooms(self, rooms):
        """Setter for rooms on drawing."""
        self._rooms = rooms

    @property
    def filename(self):
        """Drawing filename."""
        return self._filename

    @filename.setter
    def filename(self, filename):
        """Setter for drawing filename."""
        self._filename = filename

    @property
    def drawing_id(self):
        """Property with drawing ID."""
        return self._drawing_id

    @drawing_id.setter
    def drawing_id(self, drawing_id):
        """Setter for property with drawing ID."""
        self._drawing_id = drawing_id

    def rescale(self, xoffset: float, yoffset: float, scale: float) -> None:
        """Rescale the drawing by specified offset and scale."""
        for entity in self._entities:
            entity.transform(xoffset, yoffset, scale)

    def find_entity_by_id(self, entity_id: int) -> Optional[Entity]:
        """Find entity by specified ID."""
        for entity in self._entities:
            if entity._id == entity_id:
                return entity
        return None

    def add_new_room(self, canvas_id, polygon):
        """Add new room into drawing."""
        room_id = "SAP1000" + str(self._room_counter)
        self._rooms.append(
            {"room_id": room_id, "canvas_id": canvas_id, "polygon": polygon}
        )
        self._room_counter += 1
        return room_id

    def update_room_polygon(
        self,
        room_id: str,
        canvas_id: int,
        polygon: list[tuple[float, float]],
        typ: str = "?",
    ) -> None:
        """Update the polygon for specified room."""
        room = self.find_room("room_id", room_id)
        if room is not None:
            print("updating")
            print(room)
            print(polygon)
            room["canvas_id"] = canvas_id
            room["polygon"] = polygon
            room["type"] = typ

    def find_room(
        self, selector: str, value: int | str
    ) -> Optional[dict[str, str | list[tuple[float, float]] | int | None]]:
        """Find room for the specified selector and its value."""
        for room in self._rooms:
            if room[selector] == value:
                return room
        return None

    def find_room_by_room_id(
        self, canvas_id: str
    ) -> Optional[dict[str, str | list[tuple[float, float]] | int | None]]:
        """Find room for the specified room ID."""
        return self.find_room("room_id", canvas_id)

    def find_room_by_canvas_id(
        self, canvas_id: int
    ) -> Optional[dict[str, str | list[tuple[float, float]] | int | None]]:
        """Find room for the specified canvas ID."""
        return self.find_room("canvas_id", canvas_id)

    def delete_room(self, room_id):
        """Delete the whole room."""
        room = self.find_room_by_room_id(room_id)
        if room is not None:
            # print(self._rooms)
            self._rooms.remove(room)
            # print(self._rooms)

    def delete_room_polygon(self, room_id: str) -> None:
        """Delete polygon for selected room."""
        print("DELETING ROOM POLYGON")
        room = self.find_room_by_room_id(room_id)
        if room is not None:
            room["polygon"] = None
            room["canvas_id"] = None
            print(room)
            print(self._rooms)
