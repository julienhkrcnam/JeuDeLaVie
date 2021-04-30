from enum import Enum
from random import randint

class Cell:

    def __init__(self):
        self.neighbours = []

        self._status = Status.Dead

        chance_number = randint(0,2)
        if chance_number == 1:
            self.set_alive()
        
    def set_dead(self):
        self._status = Status.Dead

    def set_alive(self):
        self._status = Status.Alive
 
    def is_dead(self):
        return self._status == Status.Dead

    def is_alive(self):
        return self._status == Status.Alive

class Status(Enum):
    Alive = 'Alive'
    Dead = 'Dead'