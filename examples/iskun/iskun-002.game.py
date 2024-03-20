import moscow_robots as mr

with mr.GameIskun("iskun-002.json") as  r:

    while r.path_clear_left():
        r.step_left()
    r.step_left()
    r.step_up()
    while r.path_clear_right():
        r.step_right()
    while r.path_clear_left():
        r.fix_cell()
        r.step_left()
    r.step_up()
    #r.fix_cell()
    while r.path_clear_right():
        r.step_right()
    r.fix_cell()
    while r.path_clear_left():
        r.step_left()

