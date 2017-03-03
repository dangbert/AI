#!/usr/bin/env python3
from schedule import Schedule
from random import choice
from random import randint
from copy import deepcopy

# implement the hill climbing search algorithm for these schedules. Try each
# different heuristic to see how better schedules are made with better
# heursitics. A state in this problem is just one instance of a schedule, and
# you can change the state by changing who works what shift on what day. I
# recommend changing a state one shift at a time to see the algorithm work
# well. For hill climbing to work you want to figure out what change to the
# current schedule results in a better schedule according to the heuristic you
# are using.

def main():
    # temporary testing of value3 function
    s = Schedule(6, 40)
    s.randomize()
    #for day in s.schedule:
    #    day.morning = randint(0, s.num_workers)
    #    day.evening = randint(0, s.num_workers)
    #    day.graveyard = randint(0, s.num_workers)

    print(s.schedule)
    hillClimb(s, 2)
    print(s.schedule)


# A state in this problem is just one instance of a schedule, and you can
# change the state by changing who works what shift on what day. I reccomend
# changing a state one shift at a time to see the algorithm work well. For hill
# climbing to work you want to figure out what change to the current schedule
# results in a better schedule according to the heuristic you are using
# @param sched: schedule object
# @param heur: int (1, 2, or 3) refering to which heurstic to use in Schedule class
def hillClimb(sched, heur):
    print("---------Local Search (" + str(heur) + ")----------")

    for i in range(125):
        # pick a random shift in the schedule and see if it improves it
        cur = h(sched, heur)
        val = cur
        print("cur value: " + str(cur))
        count = 0

        # find a change that increases the heuristic
        # count is there just in case we can find anything better
        while val <= cur and count < 100:
            count = count + 1
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
            # consider not undoing if the value is the same
            if val <= cur: # undo changes
                sched.schedule[d] = oldDay

    print("final cur value: " + str(cur))



# call the appropriate heuristic function and return the value
def h(sched, heur):
    if heur == 3:
        return sched.value3()
    if heur == 2:
        return sched.value2()
    return sched.value1() # else use heuristic 1





if __name__ == "__main__":
    main()
