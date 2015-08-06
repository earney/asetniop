# Copyright (c) 2013 Hesky Fisher
# See LICENSE.txt for details.

"Launch the plover application."

import os
import shutil
import sys
import traceback

#WXVER = '2.8'
#if not hasattr(sys, 'frozen'):
#    import wxversion
#    wxversion.ensureMinimal(WXVER)

#import wx
import json
import glob

from collections import OrderedDict

#import plover.gui.main
import app
import oslayer
from oslayer import processlock
from oslayer.config import CONFIG_DIR, ASSETS_DIR
from config import CONFIG_FILE, DEFAULT_DICTIONARY_FILE, Config
from machine.sidewinder import Stenotype as sidewinder
from machine.keymap import Keymap

import _dictionary
import output

def show_error(title, message):
    """Report error to the user.

    This shows a graphical error and prints the same to the terminal.
    """
    print(message)
    #app = wx.PySimpleApp()
    #alert_dialog = wx.MessageDialog(None,
    #                                message,
    #                                title,
    #                                wx.OK | wx.ICON_INFORMATION)
    #alert_dialog.ShowModal()
    #alert_dialog.Destroy()

def init_config_dir():
    """Creates plover's config dir.

    This usually only does anything the first time plover is launched.
    """
    # Create the configuration directory if needed.
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    # Copy the default dictionary to the configuration directory.
    if not os.path.exists(DEFAULT_DICTIONARY_FILE):
        unified_dict = {}
        dict_filenames = glob.glob(os.path.join(ASSETS_DIR, '*.json'))
        for dict_filename in dict_filenames:
            unified_dict.update(json.load(open(dict_filename, 'rb')))
        ordered = OrderedDict(sorted(unified_dict.iteritems(), key=lambda x: x[1]))
        outfile = open(DEFAULT_DICTIONARY_FILE, 'wb')
        json.dump(ordered, outfile, indent=0, separators=(',', ': '))

    # Create a default configuration file if one doesn't already
    # exist.
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'wb') as f:
            f.close()


def main():
    """Launch plover."""
    try:
        # Ensure only one instance of Plover is running at a time.
        with oslayer.processlock.PloverLock():
            init_config_dir()
            config = Config()
            config.target_file = CONFIG_FILE
            #gui = plover.gui.main.PloverGUI(config)
            #gui.MainLoop()
            with open(config.target_file, 'wb') as f:
                config.save(f)

            _engine = app.StenoEngine()
            _engine.set_machine(sidewinder({'keymap': Keymap([]).default(),
                                            'arpeggiate': False}))

            _sdc=_dictionary.DictionaryCollection()
            _sdc.set_dicts(
               [_dictionary.Dictionary({
                  "a": "a", "s": "s", "e": "d", "t": "f", 
                  "n": "j", "i": "k", "o": "l", ";":"p",
                  "as": "w", "sd": "d", "df": "r", "ad": "x",
                  "sf": "c", "af": "f", "jk": "h", "kl": "l",
                  "kl": "l", "jl": "u", "k;" : "k"})
               ]
            )
            _engine.set_dictionary(_sdc)

            def consume_command(command):
                print('=>',command)

            _engine.set_output(
                   output.Output(consume_command, _engine))
            _engine.set_is_running(True)

            #steno_engine.add_stroke_listener(StrokeDisplayDialog.stroke_handler)

            import time
            while True:
               time.sleep(1)

    except oslayer.processlock.LockNotAcquiredException:
        show_error('Error', 'Another instance of Plover is already running.')
    except:
        show_error('Unexpected error', traceback.format_exc())
    os._exit(1)

if __name__ == '__main__':
    main()
