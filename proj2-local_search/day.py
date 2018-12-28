#File: day.py
#Author: Michael Neary & Max Morawski
#Description: Represents a schedule for a single day.

class Day:
    def __init__(self, worker1, worker2, worker3):
        self.morning   = worker1
        self.evening   = worker2
        self.graveyard = worker3
    
    #sets a shift to be a certain worker
    def set(self, shift, worker):
        if shift == "morning":
            self.morning = worker
        elif shift == "evening":
            self.evening = worker
        elif shift == "graveyard":
            self.graveyard = worker
        else:
            raise ValueError("{} is not a valid shift type.".format(shift))
        
    def __repr__(self):
        return "{},{},{}".format(self.morning, self.evening, self.graveyard)
