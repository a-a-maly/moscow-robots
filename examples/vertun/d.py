import moscow_robots as mrs

def proc_main():
    for _ in range(4):
        mr.step_forward()
    pass

def proc_A():
    pass

def proc_B():
    pass

def proc_C():
    pass

def proc_D():
    pass

with mrs.GameVertun("a.json") as mr:
    proc_main()

