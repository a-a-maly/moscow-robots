import sys
import json
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

class RobotData:
    def __init__(self):
        self.kind = 0
        self.x = 0
        self.y = 0
        self.dir = 0
        self.fpos = None

    def load(self, d):
        self.kind = d["kind"]
        self.x = d["x"]
        self.y = d["y"]
        self.dir = d["dir"]
        self.fpos = d.get("fpos")

    def export(self):
        res = dict()
        res["kind"] = self.kind
        res["x"] = self.x
        res["y"] = self.y
        res["dir"] = self.dir
        if self.fpos is not None:
            res["fpos"] = [self.fpos[0], self.fpos[1]]
        return res

class GameRobot:
    direction_vectors = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def next_pos(pos, d):
        x, y = pos
        dx, dy = GameRobot.direction_vectors[d % 4]
        return (x + dx, y + dy)

    def prev_pos(pos, d):
        x, y = pos
        dx, dy = GameRobot.direction_vectors[d % 4]
        return (x - dx, y - dy)


    def __init__(self, json_name):

        self.flags = [False, False]
        self.pit = 0
        self.mem = 0

        self.base_name = "".join(json_name.split(".")[:-1])
        print("base_name", self.base_name)
        with open(json_name, "r") as json_file:
            self.json_data = json.load(json_file)

        self.robot = RobotData()
        self.robot.load(self.json_data["robot"])
        self.robot_kind = self.robot.kind

        fdata = self.json_data["field"]
        self.field = None
        self.fsize = (fdata["sx"], fdata["sy"])

        ssize = (800, 800)
        fsize_minx, fsize_miny = 3, 2
        fsize_x = max(fsize_minx, self.fsize[0])
        fsize_y = max(fsize_miny, self.fsize[1])
        csize_x = ssize[0] // fsize_x
        csize_y = ssize[1] // fsize_y
        csize = min(csize_x, csize_y)
        self.csize = (csize, csize)
        self.ssize = (self.csize[0] * fsize_x, self.csize[1] * fsize_y)    

        pygame.freetype.init()
        pygame.display.init()
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        pygame.event.set_blocked(pygame.WINDOWMOVED)

        self.screen = pygame.display.set_mode(self.ssize)

        self.game_speed = 250
        self.game_mode = 0
        self.robot_alive = True


    def __enter__(self):
        self.robot_alive = True
        self.game_mode = 2 # step by step
        self.finish_step(True, False)
        return self


    def __exit__(self, t, v, tb):
        pygame.image.save(self.screen, self.base_name + ".final.png")
        self.store_state(self.base_name + ".final.json")
        ok = self.task_complete()
        print("ok:", ok)
        self.game_mode = 2 # step by step
        self.finish_step(True, False, False)
        if not self.robot_alive:
            return True

    def export_state(self):
        res = dict()
        res["alive"] = self.robot_alive
        res["complete"] = self.task_complete()
        res["robot"] = self.robot.export()
        if self.field is not None:
            if self.field.export is not None:
                res["field"] = self.field.export()
        return res

    def store_state(self, fname = None):
        state = self.export_state()
        if fname is None:
            fname = self.base_name + ".final.json"
        with open(fname, "w") as file:
            json.dump(state, file, indent='\t')


    def task_complete(self): # to be overriden
        return False

    def redraw_all(self): # to be overriden
        pass


    def finish_step(self, need_redraw=True, need_wait=True, need_raise=True):
        if need_redraw or not self.robot_alive:
            self.redraw_all()
        pygame.display.update()

        if need_wait:
            pygame.time.wait(self.game_speed)

        flag = (self.game_mode == 2)
        while True:
            pygame.event.pump()
            for ev in pygame.event.get():
                if ev.type == pygame.WINDOWSHOWN:
                    pygame.display.flip()
                    continue
                if ev.type == pygame.QUIT:
                    sys.exit("Closed by user ")
                    flag = False
                    continue
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_TAB:
                        self.game_mode = 1
                        flag = False
                    elif ev.key == pygame.K_SPACE:
                        self.game_mode = 2
                        flag = False
                    elif ev.key == pygame.K_0:
                        self.game_speed = 50
                    elif ev.key == pygame.K_1:
                        self.game_speed = 150
                    elif ev.key == pygame.K_2:
                        self.game_speed = 250
                    elif ev.key == pygame.K_3:
                        self.game_speed = 350
                    elif ev.key == pygame.K_4:
                        self.game_speed = 450
                    elif ev.key == pygame.K_5:
                        self.game_speed = 550
                    elif ev.key == pygame.K_6:
                        self.game_speed = 650
                    elif ev.key == pygame.K_7:
                        self.game_speed = 750
                    elif ev.key == pygame.K_8:
                        self.game_speed = 850
                    elif ev.key == pygame.K_9:
                        self.game_speed = 950
                    continue

            if not flag:
                break
            pygame.time.wait(10)

        if need_raise and not self.robot_alive:
            raise RuntimeError("Robot is dead")

    def pit_get(self):
        ans = self.pit
        self.finish_step(False)
        return ans

    def pit_clear(self):
        self.pit = 0
        self.finish_step(False)

    def pit_inc(self):
        self.pit += 1
        self.finish_step(False)

    def pit_dec(self):
        self.pit = max(0, self.pit - 1)
        self.finish_step(False)

    def mem_get(self):
        ans = self.mem
        self.finish_step(False)
        return ans

    def mem_clear(self):
        self.mem = 0
        self.finish_step(False)

    def mem_inc(self):
        self.mem += self.pit
        self.finish_step(False)

    def mem_dec(self):
        self.pit = max(0, self.mem - self.pit)
        self.finish_step(False)

    def memgt(self):
        ans = self.mem > self.pit
        self.finish_step(False)
        return ans

    def memlt(self):
        ans = self.mem < self.pit
        self.finish_step(False)
        return ans

    def memeq(self):
        ans = self.mem == self.pit
        self.finish_step(False)
        return ans

    def fl_get(self, idx):
        ans = self.flags[idx]
        self.finish_step(False)
        return ans

    def fl_set(self, idx, v):
        self.flags[idx] = v
        self.finish_step(False)
