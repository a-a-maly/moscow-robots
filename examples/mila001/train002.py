import moscow_robots as mrs

def proc_main():
    for _ in range(4):
        proc_A()
    pass

def proc_A():
    mr.step_forward()
    mr.add_one()
    mr.tow()
    mr.turn_right()
    mr.tow()
    mr.drop_one()
    pass

def proc_B():
    pass

def proc_C():
    pass

def proc_D():
    pass

with mrs.GameTrain("train002a.json") as mr:
    proc_main()

