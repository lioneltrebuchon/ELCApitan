from __future__ import division, print_function

import rospy

import numpy as np
import geopy as gp
from geopy.distance import geodesic
from math import ceil, floor
from nav_msgs.msg import OccupancyGrid

class Map(object):
    def __init__(self, size, origin, grid_size, len=50000):
        self.obstacles = []
        self.origin = (long_ori, lat_ori)
        self.dt = 1
        self.grid_size = grid_size
        self.dist_grid = int(geodesic(grid_size, 0).meters)
        map_size = 2 * len // self.dist_grid + 1
        self.map_array = np.zeros((map_size, map_size), dtype=bool)
        self.idx_origin = 2 * len // self.dist_grid * np.array([1, 1],
                                                               dtype=int)

    def add_obstacle(self, lat, long, alt, vel):
        d_obs = geodesic(self.origin, (long, lat))
        d_max = geodesic(self.origin,
                         (self.origin[0] + self.grid_size * self.size // 2,
                          self.origin[1] + self.grid_size * self.size // 2))
        rel_gps = (long - self.origin[0], lat - self.origin[1])
        if d_max < d_obs:
            return
            # d_size = np.abs(rel_gps) - (self.dlong * self.size // 2,
            #                             self.dlat * self.size // 2)
            # d_size = ceil(np.max(d_size[0] / self.dlong, d_size[1] / self.dlat))
            # new_map = np.zeros((size + d_size, size + d_size), dtype=bool)

        else:
            self.obstacles.append((long, lat, alt, vel))
            #  find corresponding grid in map
            idx = [int(val/self.grid_size) for val in rel_gps]
            idx = np.array(idx, dtype=int) + self.idx_origin
            self.map_array[idx[0], idx[1]] = True

            # compute unsafe area
            # for simplicity compute square area right now
            obs_dist_r = int(ceil(vel / self.dist_grid))
            self.map_array[idx[0] - obs_dist_r + 1:idx[0] + obs_dist_r - 1,
                           idx[1] - obs_dist_r + 1:idx[1] + obs_dist_r - 1] = True

    def update(self, obs_list):
        for obs in obs_list:
            # long, lat, alt, vel = obs
            self.add_obstacle(*obs)

        self.t += self.dt

    def build_msg(self):
        msg = OccupancyGrid()
        msg.info.map_load_time.data = self.dt
        msg.width = self.grid_size
        msg.height = self.grid_size
        map_lst = self.map_array.reshape((np.prod(self.map_array.shape),),
                                         order='C').tolist()
        msg.data = map_lst
        return msg


def main():



if __name__ == "__main__":
    rospy.init_node('map_node')
    main()


