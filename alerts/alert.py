from abc import ABC, abstractmethod

class Alert(ABC):
    @abstractmethod
    def update(self, data):
        pass
