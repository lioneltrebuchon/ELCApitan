"""
A* grid based planning
author: Atsushi Sakai(@Atsushi_twi)
        Nikos Kanargias (nkana@tee.gr)
See Wikipedia article (https://en.wikipedia.org/wiki/A*_search_algorithm)
"""

import matplotlib.pyplot as plt
import math
import sys
sys.path.insert(0,'../map/')
from obstrange import *

show_animation = True


class Node:

    def __init__(self, x, y, cost, pind):
        self.x = x
        self.y = y
        self.cost = cost
        self.pind = pind

    def __str__(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.cost) + "," + str(self.pind)


def calc_fianl_path(ngoal, closedset, reso):
    # generate final course
    rx, ry = [ngoal.x * reso], [ngoal.y * reso]
    pind = ngoal.pind
    while pind != -1:
        n = closedset[pind]
        rx.append(n.x * reso)
        ry.append(n.y * reso)
        pind = n.pind

    return rx, ry


def a_star_planning(sx, sy, gx, gy, ox, oy, reso, rr):
    """
    gx: goal x position [m]
    gx: goal x position [m]
    ox: x position list of Obstacles [m]
    oy: y position list of Obstacles [m]
    reso: grid resolution [m]
    rr: robot radius[m]
    """

    nstart = Node(round(sx / reso), round(sy / reso), 0.0, -1)
    ngoal = Node(round(gx / reso), round(gy / reso), 0.0, -1)
    ox = [iox / reso for iox in ox]
    oy = [ioy / reso for ioy in oy]

    obmap, minx, miny, maxx, maxy, xw, yw = calc_obstacle_map(ox, oy, reso, rr)

    motion = get_motion_model()

    openset, closedset = dict(), dict()
    openset[calc_index(nstart, xw, minx, miny)] = nstart

    while 1:
        c_id = min(
            openset, key=lambda o: openset[o].cost + calc_heuristic(ngoal, openset[o]))
        current = openset[c_id]

        # show graph
        if show_animation:
            plt.plot(current.x * reso, current.y * reso, "xc")
            if len(closedset.keys()) % 10 == 0:
                plt.pause(0.001)

        if current.x == ngoal.x and current.y == ngoal.y:
            print("Find goal")
            ngoal.pind = current.pind
            ngoal.cost = current.cost
            break

        # Remove the item from the open set
        del openset[c_id]
        # Add it to the closed set
        closedset[c_id] = current

        # expand search grid based on motion model
        for i in range(len(motion)):
            node = Node(current.x + motion[i][0],
                        current.y + motion[i][1],
                        current.cost + motion[i][2], c_id)
            n_id = calc_index(node, xw, minx, miny)

            if n_id in closedset:
                continue

            if not verify_node(node, obmap, minx, miny, maxx, maxy):
                continue

            if n_id not in openset:
                openset[n_id] = node  # Discover a new node

            tcost = current.cost + calc_heuristic(current, node)

            if tcost >= node.cost:
                continue  # this is not a better path

            node.cost = tcost
            openset[n_id] = node  # This path is the best unitl now. record it!

    rx, ry = calc_fianl_path(ngoal, closedset, reso)

    return rx, ry


def calc_heuristic(n1, n2):
    w = 1.0  # weight of heuristic
    d = w * math.sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2)
    return d


def verify_node(node, obmap, minx, miny, maxx, maxy):

    if node.x < minx:
        return False
    elif node.y < miny:
        return False
    elif node.x >= maxx:
        return False
    elif node.y >= maxy:
        return False

    if obmap[node.x][node.y]:
        return False

    return True


def calc_obstacle_map(ox, oy, reso, vr):

    minx = round(min(ox))
    miny = round(min(oy))
    maxx = round(max(ox))
    maxy = round(max(oy))
    #  print("minx:", minx)
    #  print("miny:", miny)
    #  print("maxx:", maxx)
    #  print("maxy:", maxy)

    xwidth = round(maxx - minx)
    ywidth = round(maxy - miny)
    #  print("xwidth:", xwidth)
    #  print("ywidth:", ywidth)

    # obstacle map generation
    obmap = [[False for i in range(xwidth)] for i in range(ywidth)]
    for ix in range(xwidth):
        x = ix + minx
        for iy in range(ywidth):
            y = iy + miny
            #  print(x, y)
            for iox, ioy in zip(ox, oy):
                d = math.sqrt((iox - x)**2 + (ioy - y)**2)
                if d <= vr / reso:
                    obmap[ix][iy] = True
                    break

    return obmap, minx, miny, maxx, maxy, xwidth, ywidth


def calc_index(node, xwidth, xmin, ymin):
    return (node.y - ymin) * xwidth + (node.x - xmin)


def get_motion_model():
    # dx, dy, cost
    motion = [[1, 0, 1],
              [0, 1, 1],
              [-1, 0, 1],
              [0, -1, 1],
              [-1, -1, math.sqrt(2)],
              [-1, 1, math.sqrt(2)],
              [1, -1, math.sqrt(2)],
              [1, 1, math.sqrt(2)]]

    return motion


def call_astar(sx,sy,gx,gy):
    print(__file__ + " start!!")

    # start and goal position
    #sx = 30.0  # [m]
    #sy = 2.0  # [m]
    #gx = 16.0  # [m]
    #gy = 38.0  # [m]
    grid_size = 1.0  # [m]
    robot_size = 1.5  # [m]

    ox, oy = [], []

    for i in range(40):
        ox.append(i)
        oy.append(0.0)
    for i in range(40):
        ox.append(40.0)
        oy.append(i)
    for i in range(41):
        ox.append(i)
        oy.append(40.0)
    for i in range(41):
        ox.append(0.0)
        oy.append(i)

    # Towers 
    res = 0.1  
    twr1 = [i/res for i in [2,2.8,0]]
    twr2 = [i/res for i in [1.5,1,0]]
    twr3 = [i/res for i in [3.15,0.7,0]]
    twr4 = [i/res for i in [3,2,0]]
    
    wt = 0.4/res
    r_bubble = 0.0/res
    wt_bubble = wt + r_bubble

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

    rx, ry = a_star_planning(sx, sy, gx, gy, ox, oy, grid_size, robot_size)
    return rx/10,ry/10
  
if __name__ == '__main__':
    main()
