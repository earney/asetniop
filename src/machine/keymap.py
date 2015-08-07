import json
from collections import OrderedDict

SHIFT="z"
SPACE=chr(20)

class Keymap():
    def __init__(self, assignments):
        self.keymap = OrderedDict(assignments)
        self.assignments = assignments

    def get(self):
        return self.keymap

    def __str__(self):
        return json.dumps(self.assignments)

    def to_dict(self):
        """Return a dictionary from keys to steno keys."""
        result = {}
        for stenoKey, producers in self.keymap.items():
            for key in producers:
                result[key] = stenoKey
        return result

    @staticmethod
    def from_string(string):
        assignments = json.loads(string)
        return Keymap(assignments)

    @staticmethod
    def from_rows(rows):
        """Convert a nested list of strings (e.g. from a ListCtrl) to a keymap."""
        assignments = []
        for row in rows:
            stenoKey = row[0]
            keylist = row[1].strip().split()
            assignments.append([stenoKey, keylist])
        return Keymap(assignments)

    @staticmethod
    def default():
        return Keymap.from_rows([
            ['a', 'a'],
            ["s", "s"],
            ["e", "d"],
            ["t", "f"],
            ["n", "j"],
            ["i", "k"],
            ["o", "l"],
            ["p", ";"],
            [SPACE, " "],
            #shift keys
            [SHIFT, "c"],
            [SHIFT, "v"],
            [SHIFT, "b"],
            [SHIFT, "n"],
            [SHIFT, "m"]
])
