#File: schedule.py
#Author: Michael Neary & Max Morawski
#Description: represents a schedule of employees

from random import choice
from day import Day 
import sys

try:
    from prettytable import PrettyTable
except:
    pass

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

    def toFile(self, filename):
        with open(filename,"w") as f:
            for day in self.schedule:
                f.write(str(day) + "\n")

    #load schedule from file
    #this is mostly for testing
    def load(self, filename):
        with open(filename) as f:
            lines = f.readlines()
            self.num_workers = int(lines[0].strip())
            self.num_days = int(lines[1].strip())
            self.schedule = [None]*self.num_days


            for n,d in enumerate(lines[2:]):
                m,e,g = map(int, d.split(","))
                day = Day(m,e,g)
                self.schedule[n] = day
                self.num_workers = max([m,e,g,self.num_workers])
                
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

        if type(worker) != int or worker < 0 or worker >= self.num_workers:
            msg = "{} is not a valid worker number for this schedule.".format(worker)
            raise ValueError(msg)

        if type(day) != int or day < 0 or day >= self.num_days:
            msg = "{} is not a valid day for this schedule.".format(day)
            raise ValueError(msg)

        self.schedule[day].set(shift, worker)
    
    #string representation of this schedule
    def __str__(self):

        if 'prettytable' not in sys.modules:
            out = ''
            for n,day in enumerate(self.schedule):
                out += str(n)+ ": " + str(day) + "\n"
        else:
            out = PrettyTable()
            out.add_column("", ["Morning","Evening","Graveyard"])

            for n, day in enumerate(self.schedule):
                out.add_column("Day: " + str(n), str(day).split(","))

        return str(out)

    # A schedule is considered bad if it contains a day where the same employee
    # works more than once. This heuristic should count the number of same-day
    # pairs of shifts that are not the same, and return that number. Return the
    # value as an integer.
    def value1(self):
        count = 0;

        # count the number of same-day pairs of shifts that are not the same
        for day in self.schedule:
            if day.morning != day.evening:
                count = count + 1
            if day.morning != day.graveyard:
                count = count + 1
            if day.evening != day.graveyard:
                count = count + 1
        return count

    # A schedule is considered bad if there are (1) employees who work on the
    # same day, (2) even numbered employees working on the same day as odd
    # numbered employees. Reuse what you did in value1, but this time count the
    # number of days WITHOUT an even/odd employees mix as well. Return the
    # value you calculate as an integer.
    def value2(self):
        count = self.value1()

        for day in self.schedule:
            # if no even/odd employee mix
            if day.morning % 2 == day.evening % 2 and day.evening % 2 == day.graveyard % 2:
                count = count + 1
        return count

    # A schedule is considered bad if there are (1) employees who work on the
    # same day, (2) even numbered employees working on the same day as odd
    # numbered employees, (3) employees who work a graveyard shift followed by
    # a morning shift, (4) a schedule isn't balanced, meaning that employes are
    # scheduled evenly over the number of days if you have five employees over
    # 10 days every employee would be scheduled six times for that schedule to
    # be balanced. Count the number numer of employees who are evenly
    # scheduled. Return the sum of each of these values you calculate as an
    # integer.
    def value3(self):
        count = self.value2()

        # store each employee's number of shifts in the schedule
        shifts = [0] * self.num_workers
        for n in range(self.num_days):
            day = self.schedule[n]
            shifts[day.morning] = shifts[day.morning] + 1
            shifts[day.evening] = shifts[day.evening] + 1
            shifts[day.graveyard] = shifts[day.graveyard] + 1

            # if an employee doesn't have a back to back graveyard and morning shift
            if (n+1) < self.num_days: # if next index is valid
                if day.graveyard != self.schedule[n+1].morning:
                    count = count + 1

        # number of shifts needed for employee to be balanced
        balanced = int(self.num_days * 3 / self.num_workers)
        for num in shifts:
            if num == balanced:
                count = count + 1
        return count
    
    #add any other methods you need here
