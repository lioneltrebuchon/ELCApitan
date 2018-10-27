import numpy as np
import util_connect.py
import time

# -*- coding: utf-8 -*-

createSwarmID();

N = 1;                              #number of drones
drone_id = np.array([31, 32, 33]);  #array containing the 3 drones' IDs
z_takeoff = 0.5;                    #takeoff altitude
v_takeoff = 1;                      #takeoff speed
v_travel = 1;                       #travel speed
v_landing = 0.5;                    #landing speed
target_height = 0;                  #landing height
x_base = 2.2;
y_base = 1.6;
z_base = 0;

for i in range(0,N-1):
    (x_current, y_current, z_current) = connectDrone(drone_id[i]);

for i in range(0,N-1):
    (x_desired, y_desired, z_desired, weight, package_id) = package();
    
    #(x_current, y_current, z_current, battery_percentage) = status(drone_id[i])
    
    duration = takeoff(drone_id[i], z_takeoff, v_takeoff);
    time.sleep(duration);
    
    duration = goto(drone_id[i], x_desired, y_desired, z_desired, v_travel);  
    time.sleep(duration);
    
    duration = land(drone_id[i],target_height,v_landing) ;
    time.sleep(duration);
    
    success = deliver(drone_id[i], package_id);
    
    duration = takeoff(drone_id[i], z_takeoff, v_takeoff);
    time.sleep(duration);
    
    duration = goto(drone_id[i], x_base, y_base, z_base, v_travel);
    time.sleep(duration);
    
    duration = land(drone_id[i],target_height,v_landing);
    time.sleep(duration);
    
    disconnectDrone(drone_id[id]);

