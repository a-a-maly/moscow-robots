import moscow_robots as mrs

def proc_main():
    mr.step_forward()
    mr.step_forward()
    mr.turn_right()
    mr.step_forward()
    mr.turn_right()
    mr.step_forward()
    proc_A()
    pass

def proc_A():
    for _ in range(3):
        mr.step_forward()
        mr.step_forward()
        mr.turn_right()
    pass

def proc_B():
    pass

def proc_C():
    pass

def proc_D():
    pass

with mrs.GamePolzun("polzun001a.json") as mr:
    proc_main()

