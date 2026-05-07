import MoscowRobots as mr

pitcher = 0
memory = 0
fl0 = False
fl1 = False

def proc_main():
    for _ in range(3):
        while mr.path_clear():
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

proc_main()
