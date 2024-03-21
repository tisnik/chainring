"""Unit tests for geometry related utility functions."""

from src.geometry.utils import GeometryUtils


def test_square_length_empty_length():
    """Test the static method square_length for zero length."""
    l = GeometryUtils.square_length(0, 0, 0, 0)
    assert l == 0.0


def test_square_length_horizontal():
    """Test for static method square_length for horizontal length only."""
    l = GeometryUtils.square_length(0, 0, 100, 0)
    assert l == 10000.0


def test_square_length_vertical():
    """Test for static method square_length for vertical length only."""
    l = GeometryUtils.square_length(0, 0, 0, 100)
    assert l == 10000.0


def test_square_length():
    """Test for static method square_length for length."""
    l = GeometryUtils.square_length(0, 0, 100, 100)
    assert l == 20000.0
