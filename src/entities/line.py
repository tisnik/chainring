"""Module with class that represents the two dimensional line entity."""

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


from typing import Optional

from entities.entity import Entity
from geometry.bounds import Bounds
from gui.canvas import Canvas


class Line(Entity):
    """Class that represents the two dimensional line entity."""

    def __init__(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: Optional[int],
        layer: Optional[str],
    ) -> None:
        """Construct new line from provided coordinates, color code, and layer name."""
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.layer = layer
        # graphics entity ID on the canvas
        self._id = None

    def str(self) -> str:
        """Return textual representation of line."""
        return f"L {self.color} {self.layer} {self.x1} {self.y1} {self.x2} {self.y2}"

    def as_dict(self):
        """Convert Line entity into proper dictionary."""
        return {
            "T": "L",
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2,
            "color": self.color,
            "layer": self.layer,
        }

    def draw(
        self, canvas: Canvas, xoffset: int = 0, yoffset: int = 0, scale: int = 1
    ) -> None:
        """Draw the entity onto canvas."""
        # step 1: translate
        x1 = self.x1 + xoffset
        y1 = self.y1 + yoffset
        x2 = self.x2 + xoffset
        y2 = self.y2 + yoffset
        # step 2: scale
        x1 *= scale
        y1 *= scale
        x2 *= scale
        y2 *= scale
        self._id = canvas.create_line(x1, y1, x2, y2, fill="black", tags="drawing")

    def transform(self, xoffset: float, yoffset: float, scale: float) -> None:
        """Perform the transformation of the entity into paper space."""
        self.x1 = self.x1 + xoffset
        self.y1 = self.y1 + yoffset
        self.x2 = self.x2 + xoffset
        self.y2 = self.y2 + yoffset
        self.x1 *= scale
        self.y1 *= scale
        self.x2 *= scale
        self.y2 *= scale

    def get_bounds(self) -> Bounds:
        """Compute bounds for given entity."""
        return Bounds(
            min(self.x1, self.x2),
            min(self.y1, self.y2),
            max(self.x1, self.x2),
            max(self.y1, self.y2),
        )
