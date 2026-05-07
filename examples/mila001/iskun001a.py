import moscow_robots as mrs

def proc_main():
    while mr.path_clear_right():
        mr.step_right()
        proc_A()
    pass

def proc_A():
    if mr.path_clear_up():
        mr.fix_cell()
    pass

def proc_B():
    pass

def proc_C():
    pass

def proc_D():
    pass

with mrs.GameIskun("iskun001a.json") as mr:
    proc_main()
with mrs.GameIskun("iskun001b.json") as mr:
    proc_main()

