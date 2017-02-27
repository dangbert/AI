#!/usr/bin/env python3
from schedule import Schedule

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
    s = Schedule(11, 20)
    s.randomize()
    val = s.value3()
    print("value3 = " + str(val))

if __name__ == "__main__":
    main()
