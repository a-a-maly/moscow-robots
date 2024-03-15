import moscow_robots as mr

with mr.GameRobot("vertun-002.json") as  r:
    print(type(r))

    while r.path_clear():
        r.step_forward()
    r.step_forward()
    r.turn_right()
    r.step_forward()
    r.turn_right()
    while r.path_clear():
        r.step_forward()
    r.turn_left()
    r.turn_left()
    while r.path_clear():
        r.fix_cell()
        r.step_forward()
    r.turn_right()
    r.step_forward()
    r.turn_right()
    while r.path_clear():
        r.step_forward()
    r.turn_left()
    r.turn_left()
    r.fix_cell()
    while r.path_clear():
        r.step_forward()

    

