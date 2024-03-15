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


class Entity:
    """Abstract class that represents any two dimensional entity."""

    def draw(self, canvas, xoffset, yoffset, scale):
        """Draw the entity onto canvas."""

    def transform(self, xoffset, yoffset, scale):
        """Perform the transformation of the entity into paper space."""

    def getBounds(self):
        """Compute bounds for given entity."""
