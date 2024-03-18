"""All possible modes for canvas (view, draw, select polygon etc.)."""

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

from enum import Enum


class CanvasMode(Enum):
    """All possible modes for canvas (view, draw, select polygon etc.)."""

    VIEW = (1,)
    DRAW_ROOM = (2,)
    SELECT_POLYGON_FOR_ROOM = 3
