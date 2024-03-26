"""Module with class that represents bounds of one entity or a larger entity group."""

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
from entities.arc import Arc
from entities.circle import Circle
from entities.line import Line
from entities.polyline import Polyline
from entities.text import Text
from typing import List, Union


class Bounds:
    """Class representing bounds of given entity or a larger group of entitites."""

    def __init__(
        self,
        xmin: float=sys.float_info.max,
        ymin: float=sys.float_info.max,
        xmax: float=-sys.float_info.max,
        ymax: float=-sys.float_info.max,
    ) -> None:
        """Construct new bounds using given coordinates or default values."""
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def enlarge(self, other: "Bounds") -> None:
        """Enlarge the area represented by bound."""
        self.xmin = min(self.xmin, other.xmin)
        self.ymin = min(self.ymin, other.ymin)
        self.xmax = max(self.xmax, other.xmax)
        self.ymax = max(self.ymax, other.ymax)

    def __repr__(self) -> str:
        """Return textual representation of the bound."""
        return "[{xmin}, {ymin}] - [{xmax}, {ymax}]".format(
            xmin=self.xmin, ymin=self.ymin, xmax=self.xmax, ymax=self.ymax
        )

    @staticmethod
    def compute_bounds(entities: List[Union[Line, Arc, Circle, Text, Polyline]]) -> "Bounds":
        """Compute bounds for all given entities."""
        # initial settings - empty bounds area
        bounds = Bounds()
        for entity in entities:
            bounds.enlarge(entity.get_bounds())
        return bounds
