"""
caaalle.entry_points.py
~~~~~~~~~~~~~~~~~~~~~~

This module contains the entry-point functions for the caaalle module,
that are referenced in setup.py.
"""

from sys import argv

from . import add


def main() -> None:
    """Main package entry point."""
    try:
        _, initial, number, *rest = *argv
        print(add(initial, number))
    except IndexError:
        print('🦄')
