from oslayer.keyboardcontrol import KeyboardEmulation

class Output(object):
    def __init__(self, engine_command_callback, engine):
        self.engine_command_callback = engine_command_callback
        self.keyboard_control = KeyboardEmulation()
        self.engine = engine

    def send_backspaces(self, b):
        self.CallAfter(self.keyboard_control.send_backspaces, b)

    def send_string(self, t):
        print('send_string', t)
        self.CallAfter(self.keyboard_control.send_string, t)

    def send_key_combination(self, c):
        self.CallAfter(self.keyboard_control.send_key_combination, c)

    def CallAfter(self, func, value):
        #print('CallAfter', func, value)
        func(value)

    # TODO: test all the commands now
    def send_engine_command(self, c):
        result = self.engine_command_callback(c)
        if result and not self.engine.is_running:
            self.engine.machine.suppress = self.send_backspaces
