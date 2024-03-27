"""Class representing one room on drawing."""

from typing import Optional

#
#  (C) Copyright 2017  Pavel Tisnovsky
#
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the Eclipse Public License v1.0
#  which accompanies this distribution, and is available at
#  http://www.eclipse.org/legal/epl-v10.html
#
#  Contributors:
#      Pavel Tisnovsky
#


class Room:
    """Class representing one room on drawing."""

    def __init__(self) -> None:
        """Initialize the class."""
        self.cleanup()

    def cleanup(self) -> None:
        """Perform cleanup for active room."""
        self.last_x = None
        self.last_y = None
        self.polygon_world = []
        self.polygon_canvas = []

    def last_point_exist(self) -> float | None:
        """Check if the last point (entered by user) exists."""
        return self.last_x and self.last_y

    def vertexes(self) -> int:
        """Return number of vertexes drawn by user."""
        return len(self.polygon_world)
