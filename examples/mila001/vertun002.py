import moscow_robots as mrs

def proc_main():
    proc_C()
    mr.turn_right()
    proc_A()
    pass

def proc_A():
    for _ in range(3):
        proc_B()
        mr.turn_right()
    pass

def proc_B():
    for _ in range(mr.pit_get()):
        mr.step_forward()
        mr.fix_cell()
    pass

def proc_C():
    while not mr.cell_fixed():
        mr.fix_cell()
        mr.step_forward()
        mr.pit_inc()
    pass

def proc_D():
    pass

with mrs.GameVertun("vertun002a.json") as mr:
    proc_main()

