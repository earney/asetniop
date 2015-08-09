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

num_chords={'a': '1', 's': '2', 'e': '3', 't': '4',
            SHIFT: '5', ' ': '6', 'n': '7', 'i': '8',
            'o': '9', 'p': '0',
            'a'+SHIFT: '!',
            's'+SHIFT: '@',
            'e'+SHIFT: '#',
            't'+SHIFT: '$',
            SHIFT+SHIFT: '%',
            ' '+SHIFT: '^',
            'n'+SHIFT: '&',
            'i'+SHIFT: '*',
            'o'+SHIFT: '(',
            'p'+SHIFT: ')',

            'at': '[',
            'at'+SHIFT: '{',

            'np': ']',
            'np'+SHIFT: '}',

            'es': '-',
            'es'+SHIFT: '_',
            'ae': '`',
            'ae'+SHIFT: '~',
            'io': '=',
            'io'+SHIFT: '+',
            'op': ';',
            'op'+SHIFT: ':',

            'ip': '\\',
            'io'+SHIFT: '|',

            'os': '.',
            'os'+SHIFT: '>',
            'ei': ',',
            'ei'+SHIFT: '<',
            
            'ep': "'",
            'ep'+SHIFT: '"',
            
            'ap': '?',
            'ap'+SHIFT: '/',

            'ai': '!',
            'ao': '(',
            'ps': ')',
            
            'eo': '-',
            'eo'+SHIFT: '_',

            'is': '+',
            'is'+SHIFT: '=',
}

chords={"a": "a", "s": "s", "e": "e", "t": "t", ' ': ' ',
        "n": "n", "i": "i", "o": "o", "p":"p",
        "as": "w", "es": "d", "et": "r", "ae": "x",
        "st": "c", "at": "f", "in": "h", "an": "q",
        "io": "l", "no": "u", "ip": "k", "is": "z",
        "np": "m", "en": "y", "it": "v", "nt": "b",
        "ns": "j", "ot": "g", 
        "pt": u'\uFF08',  #backspace
        SHIFT+' ': u'\uFF0D',    #enter key
        "po": ";",
        SHIFT+"po": ":",
        "eo": "-",
        SHIFT+"eo": "_",
        "ei": ",",
        SHIFT+"ei": "<",
        "so": ".",
        SHIFT+"so": ">",
        "sp": ")",
        "ao": "(",
        "ai": "!"
}


_dict={}
for _key, _value in chords.items():
    _k=_key.split()
    _k.sort()
    _key=''.join(_k)
    #_dict[_key]=_value
    _dict[(_key,)]=_value
    if _value.isalpha():
       #_dict[_key+SHIFT]=_value.upper()
       _dict[(_key+SHIFT,)]=_value.upper()

_dicts=[]
_dicts.append(_dict)

_dict={}
for _key, _value in num_chords.items():
    _k=_key.split()
    _k.sort()
    _key=''.join(_k)

    _dict[(_key,)]=_value

_dicts.append(_dict)

print(_dict)

def main():
    """Launch asetniop."""
    try:
        # Ensure only one instance of Plover is running at a time.
        with oslayer.processlock.PloverLock():
            _engine = app.StenoEngine()
            _engine.set_machine(sidewinder({'keymap': Keymap([]).default(),
                                            'arpeggiate': False}))

            for _dict in _dicts:
                _sdc=_dictionary.DictionaryCollection()
                _sdc.set_dicts([_dictionary.Dictionary(_dict)])
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
