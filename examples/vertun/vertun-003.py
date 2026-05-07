import moscow_robots as mrs

def proc_main():
    while mr.path_clear():
        mr.step_forward()
    mr.fix_cell()
    mr.turn_right()
    mr.step_forward()
    mr.fix_cell()
    pass

def proc_A():
    pass

def proc_B():
    pass

def proc_C():
    pass

def proc_D():
    pass

with mrs.GameVertun("vertun-003h.json") as mr:
    pass
    proc_main()

