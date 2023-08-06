"""
caaalle
~~~~~~

The caaalle package.
"""

__version__ = "2.1.2"

def add(initial: int=0, number: int=0) -> int:
    """Return sum of *intial* and *number*.
    :param initial: Initial value.
    :type initial: int
    :param number: Value to add to initial.
    :type number: int
    :return: Sum of initial and number.
    :rtype: int
    """
    return initial + number


def multiply(initial: int=0, number: int=0) -> int:
    """Return product of *intial* and *number*.
    :param initial: Initial value.
    :type initial: int
    :param number: Value to add to initial.
    :type number: int
    :return: Product of initial and number.
    :rtype: int
    """
    return initial * number


def pow(initial: int=0, number: int=0) -> int:
    """Return power of *intial* and *number*.
    :param initial: Initial value.
    :type initial: int
    :param number: Value to add to initial.
    :type number: int
    :return: Power of initial and number.
    :rtype: int
    """
    return initial ** number