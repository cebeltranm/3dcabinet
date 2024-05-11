from abc import ABC, abstractmethod

class BusEventLlistener(ABC):
    @abstractmethod
    def select_screen(self, screen, section):
        pass


class BusEvents(BusEventLlistener):
    _instance = None 
    _listener = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BusEvents, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        pass
    
    def set_listener(self, listener):
        self._listener = listener

    def select_screen(self, screen, section = None):
        if self._listener:
            self._listener.select_screen(screen, section)
    
    def select_color(self, color):
        if self._listener:
            self._listener.select_color(color)
