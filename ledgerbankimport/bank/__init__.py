# -*- coding: utf8 -*-

"""
Each module in this package handles importing of particular type of bank report.
"""

def unquote(str_value, quotechar='"'):
    """
    Remove quotes around given string + stripping.
    """
    result = str_value
    if str_value.startswith(quotechar) and str_value.endswith(quotechar):
        result = str_value[1:-1].strip()
    return result
