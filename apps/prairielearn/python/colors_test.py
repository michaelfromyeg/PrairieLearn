import pytest
from coloraide import Color as Base
from colors import Color, get_css_color


@pytest.mark.parametrize(
    "color, expected",
    [
        ("red", "#ff0000"),
        ("RED", "#ff0000"),
        ("correct_green", "#008c31"),
        ("none", None),
    ],
)
def test_get_css_color(color: str, expected: str) -> None:
    """
    Assert the get_css_color method returns hex strings if given valid input.

    Note that the new color constructor `Color(...)` is preferred.
    """
    assert get_css_color(color) == expected


@pytest.mark.parametrize(
    "color, expected",
    [("red", Base("srgb", [1, 0, 0], 1)), ("RED", Base("srgb", [1, 0, 0], 1))],
)
def test_color_constructor(color: str, expected: str) -> None:
    """Assert the color constructor returns a color object if given valid input."""
    assert Color(color) == expected


def test_color_constructor_custom() -> None:
    """Assert the color constructor can handle custom colors."""
    assert Color("correct_green") == Color("green3")


def test_color_constructor_error() -> None:
    """Assert the color constructor raises a ValueError if given invalid input."""
    with pytest.raises(ValueError):
        Color("none")


@pytest.mark.parametrize(
    "color",
    [
        ("red"),
        ("RED"),
        ("correct_green"),
        ("none"),
    ],
)
def test_color_match(color: str) -> None:
    """
    Assert the custom color match method returns a color object (or None).
    """
    if color == "none":
        assert Color.match(color) is None
    else:
        assert Color.match(color) is not None
