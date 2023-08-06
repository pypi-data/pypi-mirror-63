import re
from typing import Callable, Sequence, Tuple, Union

__author__ = 'Philipp Tempel'
__email__ = 'p.tempel@tudelft.nl'

DEFAULT_STRIP_REGEXP = re.compile(r'[^A-Z0-9]+', re.IGNORECASE)

DEFAULT_SPLIT_REGEXP = [
        re.compile(r'([a-z0-9])([A-Z])'),
        re.compile(r'([A-Z])([A-Z][a-z])'),
]


def replace(string: str,
            reg: Union[re.Pattern, Sequence[re.Pattern]],
            value: str) -> str:
    try:
        for reg_ in reg:
            string = reg_.sub(value, string)
    except TypeError:
        string = reg.sub(value, string)

    return string


def change_case(s: str,
                delimiter: str,
                transform: Union[
                    Callable[[str], str],
                    Tuple[Callable[[str], str], Callable[[str], str]],
                ]):
    ss: str = replace(
            replace(s, DEFAULT_SPLIT_REGEXP, "\\1\0\\2"),
            DEFAULT_STRIP_REGEXP,
            "\0")

    try:
        start = 0
        end = len(ss)
        while ss[start] == "\0":
            start += 1
        while ss[end - 1] == "\0":
            end -= 1

        # split word into pieces
        words = ss[start:end].split("\0")

        if not isinstance(transform, Tuple):
            transform = (transform, transform)

        words = [transform[0](words[0])] + [transform[1](w) for w in words[1:]]

        # words = transform[0](words[0], 0) + \
        #         + [transform(w, idx) for idx, w in enumerate(words, start=1)]

        return delimiter.join(words)
    except IndexError:
        return s


def replace_separator_by(string, sep, by):
    return re.sub(r'({})'.format(sep), by, string)


def lower_first_transform(word: str, index: int):
    """
    Lower-case the first word in a series of words

    Parameters
    ----------
    word : str
        Word to lower or upper case.
    index : int
        Index of word in original string of words. If `index == 0`, `word`
        will be lower-cased, every other word will be capitalized.

    Returns
    -------
    w : str
        Transformed word.
    """
    return word.lower() if index == 0 else word.capitalize()


def capital_first_transform(word: str, index: int):
    """
    Capital-case a single word

    Parameters
    ----------
    word : str
        Word to capital-case
    index : int
        Index of word in original string of words. If `index == 0`, the word
        will be capitalized, otherwise it will be lower-cased.

    Returns
    -------
    w : str
        Transformed word.
    """
    return word.capitalize() if index == 0 else word.lower()


def capital_transform(word: str, index: int):
    """
    Capital-case a single word

    Parameters
    ----------
    word : str
        Word to capitalize
    index : int
        Index of word in original string of words.

    Returns
    -------
    w : str
        Transformed word.
    """
    return word.capitalize()


def lower_transform(word: str, index: int):
    """
    Lower-case every word.

    Parameters
    ----------
    word : str
        Word to lower-case
    index : int
        Index of word in original string of words.

    Returns
    -------
    w : str
        Transformed word.
    """
    return word.lower()


def upper_transform(word: str, index: int):
    """
    Upper-case every word.

    Parameters
    ----------
    word : str
        Word to upper-case
    index : int
        Index of word in original string of words.

    Returns
    -------
    w : str
        Transformed word.
    """
    return word.upper()


def camel_case(s: str):
    return change_case(s, '', (str.lower,
                               lambda w: f'_{w}'
                               if w.isnumeric() else w.capitalize()))


def capital_case(s: str):
    return change_case(s, ' ', str.capitalize)


def constant_case(s: str):
    return change_case(s, '_', str.upper)


def dot_case(s: str):
    return change_case(s, '.', str.lower)


def header_case(s: str):
    return change_case(s, '-', str.capitalize)


def no_case(s: str):
    return change_case(s, ' ', str.lower)


def param_case(s: str):
    return change_case(s, '-', str.lower)


def pascal_case(s: str):
    return change_case(s, '', (str.capitalize,
                               lambda w: f'_{w}'
                               if w.isnumeric() else w.capitalize()))


def path_case(s: str):
    return change_case(s, '/', str.lower)


def sentence_case(s: str):
    return change_case(s, ' ', (str.capitalize, str.lower))


def snake_case(s: str):
    return change_case(s, '_', str.lower)


__all__ = [
        'camel_case',
        'capital_case',
        'constant_case',
        'dot_case',
        'header_case',
        'no_case',
        'param_case',
        'pascal_case',
        'path_case',
        'sentence_case',
        'snake_case',
]
