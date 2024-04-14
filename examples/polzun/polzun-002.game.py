#!python3
import moscow_robots as mr

with mr.GamePolzun("polzun-002.json") as  r:

    r.turn_left()
    r.step_forward()
    r.step_forward()
    r.turn_right()
    r.step_forward()
    r.turn_right()
    r.step_forward()
    r.step_forward()
    r.turn_left()
    r.step_forward()
    r.turn_left()
    r.step_forward()
    r.step_forward()


