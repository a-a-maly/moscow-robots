
class Robot:
    def __init__(self):
        self.kind = 0
        self.x = 0
        self.y = 0
        self.dir = 0
        self.fpos = None
        self.alive = True
        
    def load(self, d):
        self.kind = d["kind"]
        self.x = d["x"]
        self.y = d["y"]
        self.dir = d["dir"]
        self.fpos = d.get("fpos")
        self.alive = True

class Cell:
    def __init__(self):
        self.broken = False

class Field:
    def __init__(self):
        self.sx = 1
        self.sy = 1
        self.cells = [[Cell() for x in range(self.sx)] for y in range(self.sy)]
        self.hfences = [[0 for x in range(self.sx)] for y in range(self.sy - 1)]
        self.vfences = [[0 for x in range(self.sx - 1)] for y in range(self.sy)]

    def load(self, d):
        self.sx = d["sx"]
        self.sy = d["sy"]
        self.cells = [[Cell() for x in range(sx)] for i in range(sy)]
        self.hfences = [[0 for x in range(sx)] for y in range(sy - 1)]
        self.vfences = [[0 for x in range(sx - 1)] for y in range(sy)]
        _cells = d["cells"]
        for y in range(sy):
            for x in range(sx):
                self.cells[y][x].broken = _cells[y][x].get("broken", 0) 
        _vfences = d.get("vfences")
        if _vfences:
            for y in range(sy):
                for x in range(sx - 1):
                    self.vfences[y][x] = _vfences[y][x]
        _hfences = d.get("hfences")
        if _hfences:
            for y in range(sy - 1):
                for x in range(sx):
                    self.hfences[y][x] = _hfences[y][x]

f = Field()
print(f)
print(dir(f))
print("vfences", f.vfences)
print("hfences", f.hfences)
