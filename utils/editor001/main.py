import pygame

screen_resolution = (512, 1024)
pygame.display.init()
screen = pygame.display.set_mode(screen_resolution)
flag = 1
textures_n = {
    "left": "1n.png",
    "go": "2n.png",
    "right": "3n.png",
    "paint": "4n.png"
}
textures_a = {
    "left": "1a.png",
    "go": "2a.png",
    "right": "3a.png",
    "paint": "4a.png"
}
n_surface = []
a_surface = []
cell_size = [screen_resolution[0] / 4, screen_resolution[1] / 8]
yach_size = [screen_resolution[0] / 6, screen_resolution[1] / 12]
i = 0

yach_sur = pygame.image.load("rblock.png").convert()
yach_sur = pygame.transform.scale(yach_sur, yach_size)

for key in textures_n.keys():
    print(str(i), key)
    n_surface.append(pygame.image.load(textures_n[key]).convert())
    n_surface[i] = pygame.transform.scale(n_surface[i], cell_size)
    a_surface.append(pygame.image.load(textures_a[key]).convert())
    a_surface[i] = pygame.transform.scale(a_surface[i], cell_size)
    i=i+1

pol_pos = screen_resolution[1]/2

def rebuild():
    pygame.draw.rect(screen, (14, 67, 120),
                     (0, 0, screen_resolution[0], screen_resolution[1]/2))
    for i in range(len(n_surface)):
        screen.blit(n_surface[i], (cell_size[0]*i, 0))
        if i == act_but:
            screen.blit(a_surface[i], (cell_size[0]*i, 0))
    for x in range(6):
        for y in range(3):
            if commands[x+y*6] == -1:
                screen.blit(yach_sur, (yach_size[0]*x, pol_pos+yach_size[1]*y))
            else:
                i = commands[x+y*6]
                vrem_sur = pygame.transform.scale(a_surface[i], yach_size)
                screen.blit(vrem_sur, (yach_size[0]*x, pol_pos+yach_size[1]*y))
    pygame.display.flip()

def position():
    return [int(mouse[0]/yach_size[0]),int((mouse[1]-pol_pos)/yach_size[1])]


def report():
    game_name = "result.txt"
    text = ['left', 'go', 'right', 'paint']
    with open(game_name, 'w') as fp:
        for y in range(3):
            for x in range(6):
                if commands[x+y*6]>=0:
                    print(text[commands[x+y*6]], file=fp, end=" ")
                else:
                    print("_", file=fp, end=" ")
            print(file=fp)

act_but = -1

commands = []
for i in range(6*6):
    commands.append(-1)

while flag:
    flag += 1
    rebuild()
    ev = pygame.event.wait()
    if ev.type == pygame.QUIT:
        report()
        pygame.quit()
        flag = 0
    if ev.type == pygame.KEYDOWN:
        if ev.key == pygame.K_ESCAPE:
            report()
            pygame.quit()
            flag = 0
    # # checks if a mouse is clicked
    if ev.type == pygame.MOUSEBUTTONDOWN:
        mouse = pygame.mouse.get_pos()
        if mouse[1] < screen_resolution[1] / 2:
            print(ev.button)
            if mouse[1] < cell_size[1]:
                print(mouse[0], cell_size[0])
                if mouse[0] < cell_size[0]:
                    if act_but != 0:
                        act_but = 0
                    else:
                        act_but = -1
                elif mouse[0] < 2*cell_size[0]:
                    if act_but != 1:
                        act_but = 1
                    else:
                        act_but = -1
                elif mouse[0] < 3*cell_size[0]:
                    print(act_but)
                    if act_but != 2:
                        act_but = 2
                    else:
                        act_but = -1
                elif mouse[0] < 4*cell_size[0]:
                    if act_but != 3:
                        act_but = 3
                    else:
                        act_but = -1
        else:
            pos = position()
            print(pos)
            if ev.button == 3:
                commands[pos[0] + pos[1] * 6] = -1
            elif act_but != -1:
                commands[pos[0]+pos[1]*6] = act_but
                act_but = -1
            rebuild()
