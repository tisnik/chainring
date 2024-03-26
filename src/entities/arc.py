"""Module with class that represents the two dimensional arc entity."""

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


from entities.entity import Entity
from geometry.bounds import Bounds
from gui.canvas import Canvas


class Arc(Entity):
    """Class that represents the two dimensional arc entity."""

    def __init__(self, x: float, y: float, radius: float, angle1: float, angle2: float, color: int, layer: str) -> None:
        """Construct new arc from provided coordinates, angles, color code, and layer name."""
        self.x = x
        self.y = y
        self.radius = radius
        self.angle1 = angle1
        self.angle2 = angle2
        self.color = color
        self.layer = layer
        # graphics entity ID on the canvas
        self._id = None

    def str(self) -> str:
        """Return textual representation of arc."""
        return "A {color} {layer} {x} {y} {r} {a1} {a2}".format(
            color=self.color,
            layer=self.layer,
            x=self.x,
            y=self.y,
            r=self.radius,
            a1=self.angle1,
            a2=self.angle2,
        )

    def as_dict(self):
        """Convert Arc entity into proper dictionary."""
        return {
            "T": "A",
            "x": self.x,
            "y": self.y,
            "r": self.radius,
            "a1": self.angle1,
            "a2": self.angle2,
            "color": self.color,
            "layer": self.layer,
        }

    def draw(self, canvas: Canvas, xoffset: int, yoffset: int, scale: int) -> None:
        """Draw the two dimensional arc entity onto canvas."""
        extent = self.angle2 - self.angle1

        # don't use negative angle, not well supported in Tkinter
        if extent < 0:
            extent += 360

        # draw the arc, remember the canvas ID of the new graphics entity
        self._id = canvas.create_arc(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
            start=self.angle1,
            extent=extent,
            outline="black",
            style="arc",
            tags="drawing",
        )

    def transform(self, xoffset: float, yoffset: float, scale: float) -> None:
        """Perform the transformation of the entity into paper space."""
        # step 1: translate
        self.x = self.x + xoffset
        self.y = self.y + yoffset
        # step 2: scale
        self.x *= scale
        self.y *= scale
        self.radius *= scale

    def get_bounds(self) -> Bounds:
        """Compute bounds for given entity."""
        return Bounds(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
        )
