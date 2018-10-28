#from a_star_hz.py import *
from a_star2 import *
from dyn_obst import *
import sys
sys.path.insert(0,'../map/')

from static_map import *

# start and goal position
grid_size = 0.1  # [m]
gx = 3.5/grid_size  # [m]
gy = 0.5/grid_size  # [m]
robot_size = 0.15/grid_size  # [m]
r_bubble = 0.1/grid_size
xwidth = 4/grid_size
ywidth = 4/grid_size

def planner2(xcurr_self=2, ycurr_self=2, x1=0.3, y1=0.3, x2=0.3, y2=0.3):
    ox,oy = static_map(grid_size)
    xcurr_self = xcurr_self/grid_size
    ycurr_self = ycurr_self/grid_size
  # create safety bubble around drones
    x1s, y1s =(x1 - r_bubble)/grid_size,(y1 - r_bubble)/grid_size
    x2s, y2s =(x2 + r_bubble)/grid_size,(y2 + r_bubble)/grid_size

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

    if show_animation:
        plt.plot(ox, oy, ".k")
        plt.plot(xcurr_self, ycurr_self, "xr")
        plt.plot(gx, gy, "xb")
        plt.grid(True)

    rx,ry = a_star_planning(xcurr_self,xcurr_self, gx, gy, ox, oy, grid_size, robot_size) 

    if show_animation:
        plt.plot(rx, ry, "-r")
        plt.show()
    return rx[0],ry[0] 
