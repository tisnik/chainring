"""Module with abstract class that represents any two dimensional entity."""

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

from abc import ABC, abstractmethod

from geometry.bounds import Bounds


class Entity(ABC):
    """Abstract class that represents any two dimensional entity."""

    @abstractmethod
    def draw(self, canvas, xoffset, yoffset, scale):
        """Draw the entity onto canvas."""

    @abstractmethod
    def transform(self, xoffset, yoffset, scale):
        """Perform the transformation of the entity into paper space."""

    @abstractmethod
    def get_bounds(self) -> Bounds:
        """Compute bounds for given entity."""
