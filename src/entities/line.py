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

"""Module with class that represents the line."""


from entities.entity import Entity
from geometry.bounds import Bounds


class Line(Entity):
    """Class that represents the line."""

    def __init__(self, x1, y1, x2, y2):
        """Construct new line from provided coordinates."""
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        # graphics entity ID on the canvas
        self._id = None

    def str(self):
        """Return textual representation of line."""
        return "L {x1} {y1} {x2} {y2}".format(
            x1=self.x1,
            y1=self.y1,
            x2=self.x2,
            y2=self.y2)

    def asDict(self):
        return {
            "T": "L",
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2,
        }

    def draw(self, canvas, xoffset=0, yoffset=0, scale=1):
        """Draw the entity onto canvas."""
        x1 = self.x1 + xoffset
        y1 = self.y1 + yoffset
        x2 = self.x2 + xoffset
        y2 = self.y2 + yoffset
        x1 *= scale
        y1 *= scale
        x2 *= scale
        y2 *= scale
        self._id = canvas.create_line(x1, y1, x2, y2,
                                      fill="black", tags="drawing")

    def transform(self, xoffset, yoffset, scale):
        """Perform the transformation of the entity into paper space."""
        self.x1 = self.x1 + xoffset
        self.y1 = self.y1 + yoffset
        self.x2 = self.x2 + xoffset
        self.y2 = self.y2 + yoffset
        self.x1 *= scale
        self.y1 *= scale
        self.x2 *= scale
        self.y2 *= scale

    def getBounds(self):
        """Compute bounds for given entity."""
        return Bounds(min(self.x1, self.x2), min(self.y1, self.y2),
                      max(self.x1, self.x2), max(self.y1, self.y2))
