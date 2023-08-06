"""
Helper function which are used with string
"""

from typing import Iterable


def remove_chars(s: str, chars: Iterable[str]) -> str:
    """
    Removes given chars from string

    :param s: given string
    :param chars: list of string to remove from s
    :return: string without elements from chars
    """

    for char in chars:
        s = s.replace(char, '')
    return s
