import time
import matplotlib.pyplot as plt
import math
from obstrange import *
from calc_obstacle_map import *

#print(__file__ + " start!!")

def static_map(res,show_animation=False): 
    start = time.time()
    # define arena 
    w, h = 4, 4
    n_cell = w/res
    ox, oy = [], []

    # define tower
    wt, ht = 0.4, 0.4
    r_bubble = 0.1 
    wt_bubble = wt + r_bubble
    n_cell_twr = wt_bubble/res

    # define drone
    drone_size = 0.15

    # borders 
    for i in range(int(n_cell)):
        ox.append(i)
        oy.append(0.0)
    for i in range(int(n_cell)):
        ox.append(n_cell)
        oy.append(i)
    for i in range(int(n_cell)+1):
        ox.append(i)
        oy.append(n_cell)
    for i in range(int(n_cell)+1):
        ox.append(0.0)
        oy.append(i)

    # towers 
    twr1 = [2,2.8,0]
    twr2 = [1.5,1,0]
    twr3 = [3.15,0.7,0]
    twr4 = [3,2,0]

    # Tower 1
    range_bl, range_tr = obstrange(twr1,wt_bubble,res) 
    for i in range(range_bl[0],range_tr[0]):
        for j in range(range_bl[1],range_tr[1]):
            ox.append(i)
            oy.append(j)

    # Tower 2
    range_bl, range_tr = obstrange(twr2,wt_bubble,res) 
    for i in range(range_bl[0],range_tr[0]):
        for j in range(range_bl[1],range_tr[1]):
            ox.append(i)
            oy.append(j)

    # Tower 3 
    range_bl, range_tr = obstrange(twr3,wt_bubble,res) 
    for i in range(range_bl[0],range_tr[0]):
        for j in range(range_bl[1],range_tr[1]):
            ox.append(i)
            oy.append(j)

    # Tower 4 
    range_bl, range_tr = obstrange(twr4,wt_bubble,res) 
    for i in range(range_bl[0],range_tr[0]):
        for j in range(range_bl[1],range_tr[1]):
            ox.append(i)
            oy.append(j)

    # Create Obstacle map 
#    obmap, minx, miny, maxx, maxy, xwidth, ywidth = calc_obstacle_map(ox,oy,res,drone_size)
    end = time.time()
#    print(end-start) 
    if show_animation:
        plt.plot(ox, oy, ".k")
        plt.grid(True)
        plt.axis("equal")
        plt.show()
    return ox,oy, #obmap
