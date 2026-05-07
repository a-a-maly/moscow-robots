import moscow_robots as mr

pitcher = 0
memory = 0
fl0 = False
fl1 = False

def proc_main():
    for _ in range(6):
        while mr.path_clear():
            mr.step_forward()
            if mr.cell_broken():
                mr.fix_cell()
        mr.turn_right()
    pass

def proc_A():
    pass

def proc_B():
    pass

def proc_C():
    pass

def proc_D():
    pass

with mr.GameVertun("a.json") as mr:
    proc_main()
