import moscow_robots as mr

def proc_main():
    proc_C()
    r.turn_right()
    proc_A()
    pass

def proc_A():
    for _ in range(3):
        proc_B()
        r.turn_right()
    pass

def proc_B():
    for _ in range(r.pit_get()):
        r.step_forward()
        r.fix_cell()
    pass

def proc_C():
    while not r.cell_fixed():
        r.fix_cell()
        r.step_forward()
        r.pit_inc()
    pass

def proc_D():
    pass

r = mr.GameVertun("vertun002a.json")
r.__enter__()

proc_main()

r.__exit__(None, None, None)