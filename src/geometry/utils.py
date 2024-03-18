"""Class with various geometry related utility functions."""

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


class GeometryUtils:
    """Class with various geometry related utility functions."""

    @staticmethod
    def square_length(x1, y1, x2, y2):
        """Compute square length."""
        return (x1 - x2) ** 2 + (y1 - y2) ** 2
