#!/usr/bin/python3

import moscow_robots as mr

def prog_A():
    while r.path_clear():
        r.step_forward()

def prog_B():
    while r.path_clear():
        r.tow()
    #r.drop_one()

with mr.GameTrain("train-002.json") as  r:

    for _ in range(2):
        prog_A()
        r.turn_left()
        r.turn_left()
        r.add_one()
        prog_B()
        r.turn_left()
        r.step_forward()
        r.turn_left()

