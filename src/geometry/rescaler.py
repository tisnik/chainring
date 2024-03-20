"""Class to recompute scale from canvas size and computed bounds."""

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


class Rescaler:
    """Class to recompute scale from canvas size and computed bounds."""

    @staticmethod
    def compute_scale(bounds, width, height):
        """Compute scale from given bounds, width, and height."""
        xdist = bounds.xmax - bounds.xmin
        ydist = bounds.ymax - bounds.ymin
        xscale = 0.99 * width / xdist
        yscale = 0.99 * height / ydist
        scale = min(xscale, yscale)
        return -bounds.xmin, -bounds.ymin, scale

    @staticmethod
    def computeScaleForCanvas(bounds, canvas):
        """Compute scale from given bounds and canvas (with width+height)."""
        canvas_width = canvas.winfo_reqwidth()
        canvas_height = canvas.winfo_reqheight()
        return Rescaler.compute_scale(bounds, canvas_width, canvas_height)
