# -*- coding: utf-8 -*-

import re


def numeral2d3(fmt):
    """
    Convert a numeral format to d3 format.

    :return str: A string format. "" is the conversion is not possible.
    """
    if not fmt:
        return ""
    if re.match("^0\\.(0+)[ ]?%", fmt):
        digits = len(re.match("^0\\.(0+)[ ]?%", fmt).group(1))
        return f".{digits}%"
    if re.match("^0\\.(0+)", fmt):
        digits = len(re.match("^0\\.(0+)", fmt).group(1))
        return f".{digits}f"
    if fmt == "0":
        return f".0f"
    return ""
