# Copyright (c) 2013 Hesky Fisher
# See LICENSE.txt for details.

"""Unit tests for asetniop dictionary.py."""

import unittest
from dictionary import Dictionary, DictionaryCollection

_key_mappers={
"a": "a", "s": "s", "e": "d", "t": "f", "n": "j",
"i": "k", "o": "l", "p": ";",
"w": "as", "d": "sd", "r": "df", "x": "ad",
"c": "sf", "f": "af", "h": "jk", "l": "kl",
":": "l;", "u": "jl"
}

class DictionaryTestCase(unittest.TestCase):

    def test_dictionary(self):
        notifications = []
        def listener(longest_key):
            notifications.append(longest_key)
        
        d = Dictionary()
        self.assertEqual(d.longest_key, 0)
        
        d.add_longest_key_listener(listener)

        for _key, _value in _key_mappers.items():
           _k=tuple(_key)
           d[_k] = _value
           self.assertEqual(d.longest_key, 1)
           #self.assertEqual(notifications, [1])
        
        d.remove_longest_key_listener(listener)
        
if __name__ == '__main__':
    unittest.main()
