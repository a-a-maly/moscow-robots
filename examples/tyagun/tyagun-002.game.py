import moscow_robots as mr

def prog_A(r):
    while r.path_clear():
        r.step_forward()

def prog_B(r):
    while r.path_clear():
        r.tow()

with mr.GameTyagun("tyagun-002.json") as  r:

    for _ in range(2):
        prog_A(r)
        r.turn_left()
        r.turn_left()
        prog_B(r)
        r.turn_left()
        r.step_forward()
        r.turn_left()

