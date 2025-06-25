import moscow_robots as mrs

def proc_main():
    proc_A()
    mr.step_forward()
    pass

def proc_A():
    for _ in range(3):
        proc_B()
        mr.turn_left()
        mr.turn_left()
        proc_C()
        mr.turn_left()
    pass

def proc_B():
    for _ in range(3):
        mr.step_forward()
    pass

def proc_C():
    for _ in range(3):
        mr.tow()
    pass

def proc_D():
    pass

with mrs.GameTyagun("tyagun001a.json") as mr:
    proc_main()

