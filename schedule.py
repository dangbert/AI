#File: schedule.py
#Author: Michael Neary & Max Morawski
#Description: represents a schedule of employees

from random import choice
from prettytable import PrettyTable
from day import Day 

#represents a sequence of days as one cohesive schedule
class Schedule:

    #initializes a blank schedule given the numbers of workers and days
    def __init__(self, num_workers, num_days):
        self.num_workers = num_workers
        self.num_days = num_days

        self.workers = list(range(num_workers))
        self.schedule = []

        for d in range(num_days):
            day = Day(-1, -1, -1)
            self.schedule.append(day)

    #load schedule from file
    #this is mostly for testing
    def load(self, filename):
        with open(filename) as f:
            lines = f.readlines()

            self.num_days = len(lines)
            self.num_workers = 0

            for n,d in enumerate(lines):
                m,e,g = map(int, d.split())
                self.schedule[n].set("morning",m)
                self.schedule[n].set("evening",e)
                self.schedule[n].set("graveyard",g)
                self.num_workers = max([m,e,g,self.num_workers])
                
            self.num_workers += 1
            self.workers = list(range(self.num_workers))

    #randomizes the current schedule
    def randomize(self):    
        for d in range(self.num_days):
            workerA = choice(self.workers)
            workerB = choice(self.workers)
            workerC = choice(self.workers)
            day = Day(workerA, workerB, workerC)
            self.schedule[d] = day

    #set schedule on day for a shift to be a specific employee
    def set(self, day, shift, worker):

        if type(worker) != 'int' or worker < 0 or worker >= self.num_workers:
            msg = "{} is not a valid worker number for this schedule.".format(worker)
            raise ValueError(msg)

        if type(day) != 'int' or day < 0 or day >= self.num_days:
            msg = "{} is not a valid day for this schedule.".format(day)
            raise ValueError(msg)

        self.schedule[day].set(shift, worker)
    
    #string representation of this schedule
    def __str__(self):
        out = PrettyTable()
        out.add_column("", ["Morning","Evening","Graveyard"])

        for n, day in enumerate(self.schedule):
            out.add_column("Day: " + str(n), str(day).split(","))

        return str(out)

    def value(self):
        raise NotImplementedError("First heuristic is not implemented.")

    def value2(self):
        raise NotImplementedError("Second heuristic is not implemented.")

    def value3(self):
        raise NotImplementedError("Third heuristic is not implemented.")
    
    #add any other methods you need here
