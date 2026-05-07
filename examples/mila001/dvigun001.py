import moscow_robots as mrs

def proc_main():
    mr.step_forward()
    mr.turn_left()
    mr.step_forward()
    mr.turn_right()
    proc_A()
    proc_A()
    proc_A()
    proc_A()
    proc_B()
    proc_B()
    pass

def proc_A():
    proc_B()
    mr.turn_left()
    mr.turn_left()
    proc_B()
    mr.turn_right()
    mr.step_forward()
    mr.turn_right()
    pass

def proc_B():
    for _ in range(3):
        mr.step_forward()
    pass

def proc_C():
    pass

def proc_D():
    pass

with mrs.GameDvigun("dvigun001a.json") as mr:
    proc_main()

