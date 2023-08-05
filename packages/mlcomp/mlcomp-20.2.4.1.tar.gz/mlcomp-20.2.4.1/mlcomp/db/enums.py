from enum import Enum
from mlcomp.utils.misc import to_snake


class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    @classmethod
    def names(cls):
        return [e.name for e in cls]

    @classmethod
    def names_snake(cls):
        return [to_snake(n) for n in cls.names()]

    @classmethod
    def from_name(cls, name: str):
        if '_' in name or not name[0].isupper():
            return cls.names_snake().index(name)
        return cls.names().index(name)


class DagType(OrderedEnum):
    Standard = 0
    Pipe = 1


class TaskStatus(OrderedEnum):
    NotRan = 0
    Queued = 1
    InProgress = 2
    Failed = 3
    Stopped = 4
    Skipped = 5
    Success = 6


class TaskType(OrderedEnum):
    User = 0
    Train = 1
    Service = 2


class ComponentType(OrderedEnum):
    API = 0
    Supervisor = 1
    Worker = 2
    WorkerSupervisor = 3
    Client = 4


class LogStatus(OrderedEnum):
    Debug = 10
    Info = 20
    Warning = 30
    Error = 40
