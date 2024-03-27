import moscow_robots as mr

with mr.GameDvigun("dvigun-002.json") as  r:

    r.step_forward()
    r.step_forward()
    r.turn_right()
    r.turn_right()
    r.step_forward()
    for _ in range(2):
        r.turn_left()
        while r.can_move():
            r.step_forward()
