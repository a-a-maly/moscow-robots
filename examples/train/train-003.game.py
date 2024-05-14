#!/usr/bin/python3

import moscow_robots as mr


with mr.GameTrain("train-003.json") as  r:
    r.add_one()
    r.tow()
    r.tow()
    r.tow()
    r.add_one()
    r.add_one()
    r.tow()
    r.turn_right()
    r.tow()
    r.tow()
    r.add_one()
    r.tow()
    r.turn_right()
    r.tow()
    r.tow()
    r.tow()
    r.tow()
    r.tow()
    r.turn_left()
    r.turn_left()


