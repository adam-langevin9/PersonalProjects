from abc import abstractmethod, ABC
from DoublyLinkedList import DLL


class AObserver(ABC):
    @abstractmethod
    def update(self, observable):
        pass


class AObservable(ABC):
    def __init__(self):
        self.observers: DLL[AObserver] = DLL()

    def register(self, observer: AObserver):
        self.observers.append(observer)

    def unregister(self, observer: AObserver):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self)
