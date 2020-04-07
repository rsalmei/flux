from enum import Enum
from typing import Union

_VALUES = {}


class EnumSpecDescription(Enum):
    def __new__(cls, description, *spec):
        obj = object.__new__(cls)
        obj._value_ = len(_VALUES) + 1
        _VALUES[obj._value_] = obj
        obj.__description = description
        obj.__spec = spec
        return obj

    def __repr__(self):  # pragma: no cover
        return '<{}.{}: {} {!r}>'.format(self.__class__.__name__, self.name,
                                         self.value, self.__description)

    @property
    def spec(self):
        return self.__spec

    @property
    def description(self):
        return self.__description


class ModeTask(EnumSpecDescription):
    TASK = 'name, uuid, routing key, state and retries', False, False, False
    SENT = 'TASK + args/kwargs on sent state', True, False, False
    RESULT = 'TASK + result', False, True, False
    SUCCESS = 'RESULT + args/kwargs', None, True, False
    ERROR = 'TASK + error', False, False, True
    FAILURE = 'ERROR + args/kwargs', None, False, True
    OUTCOME = 'RESULT + ERROR', False, True, True
    DONE = 'SUCCESS + FAILURE', None, True, True
    THROUGH = 'SENT + SUCCESS', True, True, False
    CUTOFF = 'SENT + FAILURE', True, False, True
    DETAILS = 'SENT + DONE', True, True, True


class ModeWorker(EnumSpecDescription):
    WORKER = 'name, status and pid', False
    STATS = 'WORKER + version, load and heartbeats', True


def find_mode(constant: Union[None, int, ModeTask, ModeWorker]) \
        -> Union[None, ModeTask, ModeWorker]:
    if isinstance(constant, (type(None), ModeTask, ModeWorker)):
        return constant
    if isinstance(constant, int) and constant in _VALUES:
        return _VALUES[constant]
    raise UserWarning('Invalid mode constant.')
