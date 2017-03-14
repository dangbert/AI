#!/usr/bin/env python3
# Dan Engbert
# CMSC 471 - Spring 2017


# HOW TO RUN PROGRAM:
# run hill climbing algorithm with value3:
# python3 local_search.py --hill 3
#
# run simulated annealing algorithm with value1:
# python3 local_search.py --anneal 1


import sys
from schedule import Schedule
from random import choice
from random import randint
from random import random
from copy import deepcopy
from math import exp

# implement the hill climbing search algorithm for these schedules. Try each
# different heuristic to see how better schedules are made with better
# heursitics. A state in this problem is just one instance of a schedule, and
# you can change the state by changing who works what shift on what day. I
# recommend changing a state one shift at a time to see the algorithm work
# well. For hill climbing to work you want to figure out what change to the
# current schedule results in a better schedule according to the heuristic you
# are using.

def main():
    # check command line args
    if len(sys.argv) != 3:
        print("Error: 2 program arguments are required")
        print("       e.g. --hill 3")
        print("       or   --anneal 1")
        return
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    try:
        arg2 = int(arg2)
    except:
        tmp = arg1
        arg1 = arg2
        arg2 = tmp
        try:
            arg2 = int(arg2)
        except:
            arg2 = int(0)
    num = arg2
    if not (num == 1 or num == 2 or num == 3):
        print("Error: valid integer argument required (1, 2, or 3)")
        return
    if not (arg1 == "--anneal" or arg1 == "--hill"):
        print("Error: invalid search type argument")
        print("       use --anneal or --hill")
        return
    hill = True
    if arg1 == "--anneal":
        hill = False

    # TODO: consider generating random parameters for the schedule
    s = Schedule(7, 31)
    s.randomize()
    #for day in s.schedule:
    #    day.morning = randint(0, s.num_workers)
    #    day.evening = randint(0, s.num_workers)
    #    day.graveyard = randint(0, s.num_workers)

    print(s.schedule)
    if hill:
        hillClimb(s, num)
    else:
        simAnneal(s, num)
    print(s.schedule) # print the new schedule


# A state in this problem is just one instance of a schedule, and you can
# change the state by changing who works what shift on what day. I reccomend
# changing a state one shift at a time to see the algorithm work well. For hill
# climbing to work you want to figure out what change to the current schedule
# results in a better schedule according to the heuristic you are using
# @param sched: schedule object
# @param heur: int (1, 2, or 3) refering to which heurstic to use in Schedule class
def hillClimb(sched, heur):
    print("---------Local Search (" + str(heur) + ")----------")

    while True:
        cur = h(sched, heur) # current heuristic value
        val = cur            # new heuristic value to potentially move to
        print("cur value: " + str(cur))
        count = 0

        # find a change that increases the heuristic and move to that state
        while val <= cur and count <= 1000:
            count = count + 1

            # perform a random shift in the schedule and see if it improves it
            d = randint(0, sched.num_days-1)
            day = sched.schedule[d] # note: changing this object will change the schedule class
            oldDay = deepcopy(day)  # deep copy so orginal state will be preserved

            shift = randint(1,3)
            if shift == 1:
                day.morning = choice(sched.workers)
            if shift == 2:
                day.evening = choice(sched.workers)
            if shift == 3:
                day.graveyard = choice(sched.workers)

            val = h(sched, heur)
            if val <= cur:
                # undo changes
                sched.schedule[d] = oldDay

        # alogrithm finishes when no better nearby state is found (after 1000 attempts)
        if count > 1000:
            break
    print("hill climb complete!")
    print("final huerstic value: " + str(cur))


# simulated annealing
# like hill climbing but theres a chance of staying at the current postion even
# if its worse
# keep track of the global best
# t decreases every time you change state

#p = 0.25
#if random.random() < p)
def simAnneal(sched, heur):
    print("---------Simulated Annealing (" + str(heur) + ")----------")
    best = sched   # best schedule so far

    p = prob(23, 30, 5)
    print("prob = " + str(p))
    # temperatue starts at 100 and stops at 0
    t = 1.0
    while t > 0.001:
        # TODO: consider doing multiple iterations at each temperature
        cur = h(sched, heur)
        print("\ncur value: " + str(cur))
        # perform a random shift in the schedule and consider moving there
        d = randint(0, sched.num_days-1)
        day = sched.schedule[d] # note: changing this object will change the schedule class
        oldDay = deepcopy(day)  # deep copy so orginal state will be preserved

        shift = randint(1,3)
        if shift == 1:
            day.morning = choice(sched.workers)
        if shift == 2:
            day.evening = choice(sched.workers)
        if shift == 3:
            day.graveyard = choice(sched.workers)

        val = h(sched, heur)

        if val > cur:
            # move to better state
            # TODO: keep track of best so far
            pass

            # maybe move to other state
        else:
            r = random()
            p = prob(cur, val, t)  # acceptance probability
            #print("   prob = " + str(p), "\trandom = " + str(r))
            if not (r <= p):
                # undo changes
                sched.schedule[d] = oldDay

        t = 0.95 * t           # decrease t
    print("final huerstic value: " + str(cur))



# get a random neighbor state of a schedule
# makes a deep copy of the provided schedule
# TODO: implement this
def getNeighbor(sched):
    pass

# acceptance probability function
# cur is the heuristic value of the state we're at
# other is the heuristic value of the state we're considering going to
# t is the current temperature
def prob(cur, other, t):
    #print("\n\n")
    #print("cur = " + str(cur) + "\tother = " + str(other) + "\tt = " + str(t))
    top = float((other - cur) / t)
    #print("top = " + str(top))
    res = exp(top)
    if res > 1.0:
        res = 1.0
    return res


# call the appropriate heuristic function and return the value
def h(sched, heur):
    if heur == 3:
        return sched.value3()
    if heur == 2:
        return sched.value2()
    return sched.value1() # else use heuristic 1





if __name__ == "__main__":
    main()
