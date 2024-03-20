"""Module with class that represents the two dimensional circle entity."""

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


class Circle(Entity):
    """Class that represents the two dimensional circle entity."""

    def __init__(self, x, y, radius, color, layer):
        """Construct new circle from provided coordinates, radius, color code, and layer name."""
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.layer = layer
        # graphics entity ID on the canvas
        self._id = None

    def str(self):
        """Return textual representation of circle."""
        return "C {color} {layer} {x} {y} {r}".format(
            color=self.color, layer=self.layer, x=self.x, y=self.y, r=self.radius
        )

    def as_dict(self):
        """Convert Circle entity into proper dictionary."""
        return {
            "T": "C",
            "x": self.x,
            "y": self.y,
            "r": self.radius,
            "color": self.color,
            "layer": self.layer,
        }

    def draw(self, canvas, xoffset, yoffset, scale):
        """Draw the entity onto canvas."""
        # draw the circle, remember the canvas ID of the new graphics entity
        self._id = canvas.create_oval(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
            tags="drawing",
        )  # fill="red", tags="drawing")

    def transform(self, xoffset, yoffset, scale):
        """Perform the transformation of the entity into paper space."""
        # step 1: translate
        self.x = self.x + xoffset
        self.y = self.y + yoffset
        # step 2: scale
        self.x *= scale
        self.y *= scale
        self.radius *= scale

    def get_bounds(self):
        """Compute bounds for given entity."""
        return Bounds(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
        )
