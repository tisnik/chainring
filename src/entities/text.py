"""Module with class that represents the two dimensional text entity."""

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


class Text(Entity):
    """Class that represents the two dimensional text entity."""

    def __init__(self, x: float, y: float, text: str, color: int, layer: str) -> None:
        """Construct new text from provided coordinates, the string, color code, and layer name."""
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.layer = layer
        # graphics entity ID on the canvas
        self._id = None

    def str(self) -> str:
        """Return textual representation of text entity."""
        return "T {color} {layer} {x} {y} {t}".format(
            color=self.color,
            layer=self.layer,
            x=self.x,
            y=self.y,
            t=self.text.replace("\u00B2", "^2^"),
        )

    def as_dict(self):
        """Convert Text entity into proper dictionary."""
        return {
            "T": "T",
            "x": self.x,
            "y": self.y,
            "text": self.text,
            "color": self.color,
            "layer": self.layer,
        }

    def draw(self, canvas: Canvas, xoffset: int, yoffset: int, scale: int) -> None:
        """Draw the entity onto canvas."""
        # step 1: translate
        x = self.x + xoffset
        y = self.y + yoffset
        # step 2: scale
        x *= scale
        y *= scale
        self._id = canvas.create_text(x, y, text=self.text, fill="blue", tags="drawing")

    def transform(self, xoffset: float, yoffset: float, scale: float) -> None:
        """Perform the transformation of the entity into paper space."""
        # step 1: translate
        self.x = self.x + xoffset
        self.y = self.y + yoffset
        # step 2: scale
        self.x *= scale
        self.y *= scale

    def get_bounds(self) -> Bounds:
        """Compute bounds for given entity."""
        return Bounds(self.x, self.y, self.x, self.y)
