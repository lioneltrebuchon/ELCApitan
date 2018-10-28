#from a_star_hz.py import *
from a_star_hz import *
from dyn_obst import *
import sys
sys.path.insert(0,'../map/')

from static_map import *
from calc_obstacle_map import *

import matplotlib.pyplot as plt
show_animation = True

# start and goal position
grid_size = 0.1  # [m]
sx = 0.0  # [m]
sy = 0.0  # [m]
gx = 0.5/grid_size  # [m]
gy = 0.5/grid_size  # [m]
robot_size = 0.15  # [m]


def planner(xcurr_self=2, ycurr_self=2, x1=0.3, y1=0.3, x2=0.3, y2=0.3):
    xcurr_self = xcurr_self/grid_size
    ycurr_self = ycurr_self/grid_size

    # Get static map
    ox,oy,obmap_static = static_map(grid_size) 

    #stuff for a_star
    minx = round(min(ox))
    miny = round(min(oy))      
    maxx = round(max(ox))      
    maxy = round(max(oy))      
    xwidth = round(maxx - minx)    
    ywidth = round(maxy - miny)

    # create safety bubble around drones
    x1s, y1s = x1 - 0.1, y1 - 0.1
    x2s, y2s = x2 + 0.1, y2 + 0.1

    #Create Range of other drones
    drone1_bl, drone1_tr = obstrange([x1s,y1s],robot_size,grid_size)
    drone2_bl, drone2_tr = obstrange([x2s,y2s],robot_size,grid_size)
    
    # create moving obstacle ranges
    x1range, y1range, obmap_dyn1 = dyn_obst(drone1_bl,drone1_tr,xwidth,ywidth)
    x2range, y2range, obmap_dyn2 = dyn_obst(drone2_bl,drone2_tr,xwidth,ywidth)

    # Append position of other drones 
    ox.extend(x1range)
    ox.extend(x2range)
    oy.extend(y1range)
    oy.extend(y2range) 

    obmap = obmap_static + obmap_dyn1 + obmap_dyn2 

    if show_animation:
        plt.plot(ox, oy, ".k")
        plt.plot(sx, sy, "xr")
        plt.plot(gx, gy, "xb")
        plt.grid(True)
        rx, ry = a_star_planning(xcurr_self, ycurr_self, gx, gy, ox, oy, grid_size, robot_size, obmap, minx, miny, maxx, maxy, xwidth, ywidth)

        plt.plot(rx, ry, "-r")
        plt.show()
    return rx[0],ry[0] 
