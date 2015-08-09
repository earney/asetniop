# Copyright (c) 2010-2011 Joshua Harlan Lifton.
# See LICENSE.txt for details.

# TODO: unit test this file

"""Generic stenography data models.

This module contains the following class:

Stroke -- A data model class that encapsulates a sequence of steno keys.

"""

import re

def normalize_steno(strokes_string):
    """Convert steno strings to one common form."""
    strokes = [strokes_string]
    normalized_strokes = []
    for stroke in strokes:
        if '#' in stroke:
            stroke = stroke.replace('#', '')
            if not re.search('[0-9]', stroke):
                stroke = '#' + stroke
        has_implicit_dash = bool(set(stroke) & IMPLICIT_HYPHENS)
        if has_implicit_dash:
            stroke = stroke.replace('-', '')
        if stroke.endswith('-'):
            stroke = stroke[:-1]
        normalized_strokes.append(stroke)
    return tuple(normalized_strokes)

KEY_NUMBERS = {}

class Stroke:
    """A standardized data model for stenotype machine strokes.

    This class standardizes the representation of a stenotype chord. A stenotype
    chord can be any sequence of stenotype keys that can be simultaneously
    pressed. Nearly all stenotype machines offer the same set of keys that can
    be combined into a chord, though some variation exists due to duplicate
    keys. This class accounts for such duplication, imposes the standard
    stenographic ordering on the keys, and combines the keys into a single
    string (called RTFCRE for historical reasons).

    """

    IMPLICIT_HYPHEN = set()

    def __init__(self, keys):
        """Create a steno stroke by formatting steno keys.

        Arguments:

        keys -- A sequence of pressed keys.

        """
        # Remove duplicate keys and save local versions of the input 
        # parameters.
        keys_set = set(keys)
        keys = list(keys_set)

        # Order the steno keys so comparisons can be made.
        keys.sort() #(key=lambda x: KEY_ORDER.get(x, -1))
         
        # Convert strokes involving the number bar to numbers.
        if '#' in keys:
            numeral = False
            for i, e in enumerate(keys):
                if e in KEY_NUMBERS:
                    keys[i] = KEY_NUMBERS[e]
                    numeral = True
            if numeral:
                keys.remove('#')
        
        if keys_set:
            self.rtfcre = ''.join(key.strip('-') for key in keys)

        self._keys = keys

        # Determine if this stroke is a correction stroke.
        self.is_correction = (self.rtfcre == '*')

    def __str__(self):
        if self.is_correction:
            prefix = '*'
        else:
            prefix = ''

    def __eq__(self, other):
        return (isinstance(other, Stroke)
                and self._keys == other._keys)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self)
