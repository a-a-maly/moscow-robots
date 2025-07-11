import moscow_robots as mrs

def proc_main():
    while mr.has_to_add():
        mr.add_one()
        mr.tow()
        mr.tow()
        mr.tow()
    pass

def proc_A():
    pass

def proc_B():
    pass

def proc_C():
    pass

def proc_D():
    pass

with mrs.GameTrain("train001a.json") as mr:
    proc_main()

