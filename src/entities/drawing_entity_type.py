"""Enumeration with all entity types that can be used in drawings."""

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


from enum import Enum


class DrawingEntityType(Enum):
    """Enumeration with all entity types that can be used in drawings."""

    UNKNOWN = (1,)
    LINE = (2,)
    CIRCLE = (3,)
    ARC = (4,)
    TEXT = (5,)
    POLYLINE = (6,)
    ATTRIB = 7
