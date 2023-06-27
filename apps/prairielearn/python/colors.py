"""
Custom colors for the PrarieLearn project based on Coloraide.

Based on https://gist.github.com/facelessuser/0b129c1faf7f3f59c0de40eeaaab5691/.
"""
import re
from typing import Any, Dict, Optional, Tuple

from coloraide import Color
from coloraide import algebra as alg
from coloraide.css import serialize
from coloraide.spaces.srgb.css import sRGB

# Match the pattern of a PL color name;
# only accepts numbers, lowercase letters, and a single underscore
RE_PL_COLORS = re.compile(r"(?i)\b([0-9a-z][0-9a-z_]{2,})\b")

# Colors used in /public/stylesheets/colors.css
# includes additional aliases (e.g, "red3" also known as "incorrect_red")
PL_COLORS_NAME_MAP: Dict[str, Tuple[Any, ...]] = {
    "blue1": (57, 213, 255, 255),
    "blue2": (18, 151, 224, 255),
    "blue3": (0, 87, 160, 255),
    "brown": (142, 92, 59, 255),
    "brown1": (246, 196, 163, 255),
    "brown2": (206, 156, 123, 255),
    "brown3": (142, 92, 59, 255),
    "correct_green": (0, 140, 49, 255),
    "gray": (144, 144, 144, 255),
    "gray1": (224, 224, 224, 255),
    "gray2": (144, 144, 144, 255),
    "gray3": (80, 80, 80, 255),
    "green1": (142, 255, 193, 255),
    "green2": (46, 204, 113, 255),
    "green3": (0, 140, 49, 255),
    "incorrect_red": (183, 28, 12, 255),
    "orange1": (255, 220, 181, 255),
    "orange2": (255, 146, 107, 255),
    "orange3": (243, 130, 91, 255),
    "pink1": (255, 188, 216, 255),
    "pink2": (250, 92, 152, 255),
    "pink3": (186, 28, 88, 255),
    "purple1": (220, 198, 224, 255),
    "purple2": (155, 89, 182, 255),
    "purple3": (94, 20, 125, 255),
    "red1": (255, 204, 188, 255),
    "red2": (255, 108, 92, 255),
    "red3": (183, 28, 12, 255),
    "turquoise1": (94, 250, 247, 255),
    "turquoise2": (39, 203, 192, 255),
    "turquoise3": (0, 139, 128, 255),
    "yellow1": (253, 227, 167, 255),
    "yellow2": (245, 171, 53, 255),
    "yellow3": (216, 116, 0, 255),
}

PL_COLORS_VALUE_MAP = dict([(v, k) for k, v in PL_COLORS_NAME_MAP.items()])


class PrarieLearnColor(sRGB):
    """Custom sRGB class to handle custom PrarieLearn colors, via Coloraide."""

    def match(self, string, start=0, fullmatch=True):
        """
        Match a color string, first trying PrarieLearn.
        If no match is found, defaults to sRGB class' implementation.
        """
        # Match the string using fullmatch if requested
        match = (
            RE_PL_COLORS.fullmatch(string, start)
            if fullmatch
            else RE_PL_COLORS.match(string, start)
        )

        if match:
            # See if we can find the name
            name = match.group(1)
            values = PL_COLORS_NAME_MAP.get(name.lower(), None)

            if values is not None:
                # Normalize back to 0 - 1
                values = [c / 255 for c in values]
                # Return the coordinates and transparency separate,
                # also include the match end position.
                return (values[:-1], values[-1]), match.end(1)

        # Couldn't find custom colors, so use the default color matching.
        return super().match(string, start, fullmatch)

    def to_string(
        self,
        parent,
        *,
        alpha=None,
        precision=None,
        fit=True,
        none=False,
        color=False,
        hex=False,  # pylint: disable=redefined-builtin
        names=False,
        comma=False,
        upper=False,
        percent=False,
        compress=False,
        **kwargs,
    ) -> str:
        """Convert to string."""

        if names:
            # Get alpha and coordinates resolving undefined values as required
            alpha = serialize.get_alpha(parent, alpha, False, False)
            if alpha is None:
                alpha = 1
            coords = serialize.get_coords(parent, fit, False, False) + [alpha]

            # See if the color value is a match, if so, return the string
            result = PL_COLORS_VALUE_MAP.get(
                tuple([alg.round_half_up(c * 255) for c in coords]), None
            )
            if result is not None:
                return result

        # Color name not requested, or there was no color match, use default serialization.
        return super().to_string(
            parent,
            alpha=alpha,
            precision=precision,
            fit=fit,
            none=none,
            color=color,
            hex=hex,
            names=names,
            comma=comma,
            upper=upper,
            percent=percent,
            compress=compress,
            **kwargs,
        )


Color.register(PrarieLearnColor(), overwrite=True)


def get_css_color(name: str) -> Optional[str]:
    """
    Tries to look up a hex code value from a named css color, otherwise will
    return None if not a valid color.
    """
    name = name.lower()

    if Color.match(name):
        return Color(name).to_string(hex=True)

    return None
