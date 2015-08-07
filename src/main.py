"Launch the plover application."

import os
import shutil
import sys
import traceback
import itertools

import json
import glob

from collections import OrderedDict

import app
import oslayer
from oslayer import processlock
from machine.sidewinder import Stenotype as sidewinder
from machine.keymap import Keymap, SHIFT

import _dictionary
import output


chords={"a": "a", "s": "s", "e": "e", "t": "t", ' ': ' ',
        "n": "n", "i": "i", "o": "o", "p":"p",
        "as": "w", "es": "d", "et": "r", "ae": "x",
        "st": "c", "at": "f", "in": "h", "an": "q",
        "io": "l", "no": "u", "ip": "k", "is": "z",
        "np": "m", "en": "y", "it": "v", "nt": "b",
        "ns": "j", "ot": "g", "pt": chr(8),  #backspace
        chr(14)+' ': '\\n',    #enter key
        "po": ";",
}


_dict={}
for _key, _value in chords.items():
    _dict[(_key,)]=_value
    _dict[(SHIFT+_key,)]=_value.upper()
    _dict[(_key+SHIFT,)]=_value.upper()
    if len(_key) > 1:
       _perms = ["".join(x) for x in itertools.permutations(_key, len(_key))]
       for _perm in _perms:
           _dict[(_perm,)]=_value

       _perms = ["".join(x) for x in itertools.permutations(_key+SHIFT, len(_key+SHIFT))]
       for _perm in _perms:
           _dict[(_perm,)]=_value.upper()


print(_dict)


def main():
    """Launch asetniop."""
    try:
        # Ensure only one instance of Plover is running at a time.
        with oslayer.processlock.PloverLock():
            _engine = app.StenoEngine()
            _engine.set_machine(sidewinder({'keymap': Keymap([]).default(),
                                            'arpeggiate': False}))

            _sdc=_dictionary.DictionaryCollection()
            _sdc.set_dicts(
               [_dictionary.Dictionary(_dict)]
            )
            _engine.set_dictionary(_sdc)

            def consume_command(command):
                print('=>',command)

            _engine.set_output(
                   output.Output(consume_command, _engine))
            _engine.set_is_running(True)

            import time
            while True:
               time.sleep(1)

    except oslayer.processlock.LockNotAcquiredException:
        print('Error: Another instance of Plover is already running.')
    except:
        print('Unexpected error: %s' % traceback.format_exc())
    os._exit(1)

if __name__ == '__main__':
    main()
