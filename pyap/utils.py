# -*- coding: utf-8 -*-

"""
    pyap.utils
    ~~~~~~~~~~~~~~~~

    This module provides some utility functions.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""

import re
import string
from typing import Any, List, Union

DEFAULT_FLAGS = re.VERBOSE | re.UNICODE


def str_list_to_upper_lower_regex(str_list: List[str]) -> str:
    regex = "|".join(set(str_list)).lower()
    for letter in string.ascii_lowercase:
        regex = regex.replace(
            letter, "[{upper}{lower}]".format(upper=letter.upper(), lower=letter)
        )

    return regex


def street_type_list_to_regex(street_type_list: list[str]) -> str:
    """Converts a list of street types into a regex."""
    street_types = str_list_to_upper_lower_regex(street_type_list)

    street_types = street_types.replace("|", r"\b|\b")
    street_types = r"\b" + r"(?:" + street_types + r")" + r"\b\.?"
    return street_types


def match(
    regex: Union[str, re.Pattern[str]], string: str, flags: re.RegexFlag = DEFAULT_FLAGS
) -> Union[re.Match[str], None]:
    """Utility function for re.match"""
    return re.match(regex, string, flags=flags)


def findall(
    regex: Union[str, re.Pattern[str]], string: str, flags: re.RegexFlag = DEFAULT_FLAGS
) -> List[Any]:
    """Utility function for re.findall"""
    return re.findall(regex, string, flags=flags)


def finditer(
    regex: Union[str, re.Pattern[str]], string: str, flags: re.RegexFlag = DEFAULT_FLAGS
) -> List[re.Match[str]]:
    """Utility function for re.finditer"""
    return list(re.finditer(regex, string, flags=flags))


def unicode_str(string: str) -> str:
    """Return Unicode string"""
    return string
