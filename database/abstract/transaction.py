from abc import abstractmethod, ABC


class Transaction(ABC, object):
    @abstractmethod
    def __init__(self, *args, **kwargs): pass

    @abstractmethod
    def begin(self): pass

    @abstractmethod
    def end(self): pass

    @property
    @abstractmethod
    def data(self): pass
