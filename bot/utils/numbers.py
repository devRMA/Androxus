# MIT License

# Copyright(c) 2021-2022 Rafael

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from re import sub
from typing import Any


def is_number(string: Any) -> bool:
    """
    Check if a string is a number.

    Args:
        string (str): The string to check.

    Returns:
        bool: True if it is a number, False otherwise.

    """
    if not len(string) >= 1:
        return False
    if not isinstance(string, str):
        string = str(string)
    if string.isdecimal() or string.isnumeric():
        return True
    try:
        float(string)
    except ValueError:
        try:
            float(string.replace(',', '.'))
        except ValueError:
            return False
        else:
            return True
    else:
        return True


def format_numbers(number: Any, br: bool = True, truncate: bool = False) -> str:
    """
    Format a number to a human-readable format.

    Args:
        number (Any): The number to format.
        br (bool): Flag that will activate or not the Brazilian
            format: "100,000.00". If it has been disabled, it will
            output like this "100,000.00".
        truncate (bool): It will define whether or not to cut the
            decimal places.

    Returns:
        str: The formatted number.

    Examples:
        >>> format_numbers(123456789)
        '123.456.789'
        >>> format_numbers(3.141592)
        '3,1415'
        >>> format_numbers(3.141592, truncate=True)
        '3,14'

    """
    if not is_number(str(number)):
        return number

    if truncate:
        number = sub(r'^(\d+\.\d{,2})\d*$', r'\1', str(number))

    number = str(number).split('.')
    decimal = number[-1] if len(number) > 1 else ''
    decimal = decimal if decimal.strip('0') else ''
    number = number[0]

    separator = '.' if br else ','
    decimal_separator = ''

    if len(decimal) > 0:
        decimal_separator = ',' if br else '.'

    number = f'{int(number):_}'.replace('_', separator)
    return f'{number}{decimal_separator}{decimal}'
