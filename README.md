# Local Search

### PURPOSE:
To implement the simulated annealing and hill climbing algorithm in Python to optimize the work schedule of employees by maximizing a heuristic function.


### HOW IT WORKS:
The Schedule class (defined in schedule.py) represents an employee work schedule.
A schedule can be initiliazed with a custom number of employees and length (number of days).

Each day in the schedule consists of 3 shifts which are each filled by 1 employee.
There are 3 hueristic functions defined in the schedule class which can be picked from through a command line argument.
The schedules can be optmizized using either the hill climbing algorithm or simulated annealing algoritm (implemented in local_search.py)

The simulate annealing and hill climbing algorithms are implemented in local_search.py (functions ````hillClimb```` and ````simAnneal````)

### HOW TO RUN:
First parameter: either ````--hill```` or ````--anneal```` (selects which local search algorithm to use)
Second parameter: either ````1````, ````2````, or ````3```` (selects which heuristic function to use)
A random schedule is initially generated and then optimized according to the command line arguments.

Examples:
* ````./local_search.py --hill 3```` optimize a schedule using the hill climbing algorithm and heuristic function 3
* ````./local_search.py --anneal 1```` optimize a schedule using the simulated annealing algorithm and heuristic function 1

### NOTE:
This was created as a learning exercise but the heuristic function can be modified as desired for other use. 
