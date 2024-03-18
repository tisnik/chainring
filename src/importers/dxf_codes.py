"""List of all supported numeric codes used in DXF files."""

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


class DxfCodes:
    """List of all supported numeric codes used in DXF files."""

    TEXT_STRING = 0
    PRIMARY_TEXT = 1
    NAME = 2
    TEXT2 = 3
    TEXT3 = 4
    ENTITY_HANDLE = 5
    LINETYPE = 6
    TEXT_STYLE = 7
    LAYER_NAME = 8
    VARIABLE_NAME = 9
    X1 = 10
    Y1 = 20
    Z1 = 30
    X2 = 11
    Y2 = 21
    Z2 = 31
    X3 = 12
    Y3 = 22
    Z3 = 32
    ELEVATION = 38
    THICKNESS = 39
    RADIUS = 40  # 41-48 other floating point values
    ANGLE1 = 50
    ANGLE2 = 51  # 52-58 other angles
    VISIBILITY = 60
    COLOR = 62
    COMMENT = 999
    MIRROR = 230
