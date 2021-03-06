# See LICENSE.txt for details.

"Manager for stenotype machines types."

from machine.sidewinder import Stenotype as sidewinder

class NoSuchMachineException(Exception):
    def __init__(self, id):
        self._id = id

    def __str__(self):
        return 'Unrecognized machine type: {}'.format(self._id)

class Registry(object):
    def __init__(self):
        self._machines = {}
        self._aliases = {}

    def register(self, name, machine):
        self._machines[name] = machine

    def add_alias(self, alias, name):
        self._aliases[alias] = name

    def get(self, name):
        try:
            return self._machines[self.resolve_alias(name)]
        except KeyError:
            raise NoSuchMachineException(name)

    def get_all_names(self):
        return self._machines.keys()
        
    def resolve_alias(self, name):
        try:
            return self._aliases[name]
        except KeyError:
            return name

machine_registry = Registry()
machine_registry.register('NKRO Keyboard', sidewinder)
machine_registry.add_alias('Microsoft Sidewinder X4', 'NKRO Keyboard')
