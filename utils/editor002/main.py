import pygame

csize = 64
hwidth = 6
fwidth = 12
fheight = 12

cmds = []

cmd0 = [[i, "rblock" + i] for i in "123456"]
cmds.append(cmd0)
cmd1 = [("rfwd", "rfwd"), ("rtleft", "rtleft"), ("rtright", "rtright"), ("rfix", "rfix")]
cmds.append(cmd1)




prog  = [[None for x in range(hwidth)] for y in range(fheight)]
progb = [[None for x in range(hwidth)] for y in range(fheight)]


pygame.display.init()
screen_resolution = (fwidth * csize, fheight * csize)
screen = pygame.display.set_mode(screen_resolution)

t = pygame.image.load("rblock.png").convert_alpha()
prog_bg = pygame.transform.scale(t, (csize, csize))

cmdst = []
for line in cmds:
    cmdstl = []
    for cmd in line:
        t = pygame.image.load(cmd[1] + ".png").convert_alpha()
        t = pygame.transform.scale(t, (csize * 4 // 5, csize * 4 // 5))
        cmdstl.append(t)
    cmdst.append(cmdstl)

pos_active = (0, 0)
flag_not = False
flag_loop = False

def redraw():
    screen.fill((0, 0, 255))
    for y in range(fheight):
        for x in range(hwidth):
            bx, by = (csize * (x + hwidth), csize * y)
            
            screen.blit(prog_bg, (bx, by))
            p = prog[y][x]
            if p:
                psize = p[1].get_size()
                ax = (csize - psize[0]) // 2
                ay = (csize - psize[1]) // 2
                screen.blit(p[1], (bx + ax, by + ay))

    for y in range(len(cmds)):
        for x in range(len(cmds[y])):
            bx, by = (csize * x, csize * y)
            t = cmdst[y][x]
            if pos_active == (x, y):
                screen.blit(prog_bg, (bx, by))
            if t:
                psize = t.get_size()
                ax = (csize - psize[0]) // 2
                ay = (csize - psize[1]) // 2
                screen.blit(t, (bx + ax, by + ay))

def decode_position(pos):
    x, y = pos
    ty = y // csize
    if not (0 <= ty < fheight):
        return None
    tx = x // csize
    if not (0 <= tx < fwidth):
        return None
    return (tx // hwidth, tx % hwidth, ty)

def do_click(pos):
    global pos_active
    dpos = decode_position(pos)
    if not dpos:
        return False
    h, x, y = dpos
    if h:
        # program pane
        cmd  = cmds [pos_active[1]][pos_active[0]][0]
        cmdt = cmdst[pos_active[1]][pos_active[0]]
        
        if prog[y][x] and cmd == prog[y][x][0]:
            prog [y][x] = progb[y][x]
            progb[y][x] = None
        else:
            progb[y][x] = prog[y][x]
            prog [y][x] = (cmd, cmdt)
        return True
    else:
        #command pane
        if y >= len(cmds) or x >= len(cmds[y]):
            return False
        pos_active = (x, y)
        return True


def dump_program(prog):
    for line in prog:
        l = len(line)
        while l > 0:
            if line[l - 1]: break
            l -= 1
        for cmd in line[:l]:
            if cmd:
                print(cmd[0], end=' ')
            else:
                print('_', end = ' ')
        print()


flag_dirty = True
while True:
    if flag_dirty:
        flag_dirty = False
        redraw()
        pygame.display.flip()

    pygame.time.wait(10)
    ev = pygame.event.wait()

    if ev.type == pygame.WINDOWSHOWN:
        pygame.display.flip()
        continue

    if ev.type == pygame.QUIT:
        break

    if ev.type == pygame.KEYDOWN:
        if ev.key == pygame.K_ESCAPE:
            break

    if ev.type == pygame.MOUSEBUTTONDOWN:
        mpos = ev.pos
        if ev.button == 1:
            flag_dirty = do_click(ev.pos)
            continue


dump_program(prog)
pygame.quit()
