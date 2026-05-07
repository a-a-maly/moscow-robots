import moscow_robots as mr

pitcher = 0
memory = 0
fl0 = False
fl1 = False

def proc_main():

    number_of_steps = 0
    number_of_cells_fixed = 0

    for _ in range(6):
        while mr.path_clear():
            mr.step_forward()
            number_of_steps += 1
            if mr.cell_broken():
                mr.fix_cell()
                number_of_cells_fixed += 1
        mr.turn_right()
    print(number_of_steps, number_of_cells_fixed)

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
