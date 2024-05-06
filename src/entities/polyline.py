"""Module with class that represents the two dimensional polyline entity."""

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

from entities.entity import Entity
from geometry.bounds import Bounds
from gui.canvas import Canvas


class Polyline(Entity):
    """Class that represents the two dimensional polyline entity."""

    def __init__(
        self,
        points_x: list[float],
        points_y: list[float],
        color: Optional[int],
        layer: Optional[str],
    ) -> None:
        """Construct new text from provided starting coordinates, color code, and layer name."""
        self.points_x = points_x
        self.points_y = points_y
        self.color = color
        self.layer = layer
        # graphics entity ID on the canvas
        self._id = None

    @staticmethod
    def point_list_to_str(point_list):
        """Convert list of coordinates into string, space is used as a separator."""
        return " ".join([str(i) for i in point_list])

    def str(self):
        """Return textual representation of polyline entity."""
        return f"P {self.color} {self.layer} {len(self.points_x)} {Polyline.point_list_to_str(self.points_x)} {Polyline.point_list_to_str(self.points_y)}"

    def as_dict(self):
        """Convert Polyline entity into proper dictionary."""
        return {
            "T": "P",
            "xpoints": self.points_x,
            "ypoints": self.points_y,
            "color": self.color,
            "layer": self.layer,
        }

    def draw(
        self, canvas: Canvas, xoffset: int = 0, yoffset: int = 0, scale: int = 1
    ) -> None:
        """Draw the entity onto canvas."""
        points = []
        for i in range(len(self.points_x)):
            x = self.points_x[i] + xoffset
            y = self.points_y[i] + yoffset
            x *= scale
            y *= scale
            points.append(x)
            points.append(y)
        # special polyline used for selecting room
        if self.layer is not None and self.layer == "CKPOPISM_PLOCHA":
            new_object = canvas.create_polygon(
                points, fill="", width=2, activeoutline="red", outline="green"
            )
            self._id = new_object
            canvas.tag_bind(
                new_object,
                "<ButtonPress-1>",
                lambda event, new_object=new_object: canvas.on_polygon_for_room_click(
                    new_object
                ),
            )
        # just a regular polyline
        else:
            self._id = canvas.create_polygon(points, fill="", outline="green")

    def transform(self, xoffset: float, yoffset: float, scale: float) -> None:
        """Perform the transformation of the entity into paper space."""
        for i in range(len(self.points_x)):
            # step 1: translate
            self.points_x[i] = self.points_x[i] + xoffset
            self.points_y[i] = self.points_y[i] + yoffset
            # step 2: scale
            self.points_x[i] *= scale
            self.points_y[i] *= scale

    def get_bounds(self) -> Bounds:
        """Compute bounds for given entity."""
        xmin = sys.float_info.max
        ymin = sys.float_info.max
        xmax = -sys.float_info.max
        ymax = -sys.float_info.max

        # x bounds for all vertexes
        for x in self.points_x:
            if x < xmin:
                xmin = x
            if x > xmax:
                xmax = x

        # y bounds for all vertexes
        for y in self.points_y:
            if y < ymin:
                ymin = y
            if y > ymax:
                ymax = y

        return Bounds(xmin, ymin, xmax, ymax)
