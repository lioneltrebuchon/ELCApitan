import numpy as np
from util_connect import *
import time

# -*- coding: utf-8 -*-

def reached_pos(id,des_pos,accuracy):
   (x,y,z,battery_percentage) = status(id)
   if abs(des_pos[0]-x) <= accuracy and abs(des_pos[1]-y) <= accuracy and abs(des_pos[2]-z) <= accuracy:
       return True
   else:
       return False

N = 1;                              #number of drones
drone_id = np.array([31, 32, 33]);  #array containing the 3 drones' IDs
z_takeoff = 0.5;                    #takeoff altitude
v_takeoff = 1;                      #takeoff speed
v_travel = 1;                       #travel speed
v_landing = 0.5;                    #landing speed
target_height = 0;                  #landing height
x_base = 2.2;                       #base coordinates
y_base = 1.6;
z_base = 0;
accuracy = 0.2;                     #standard deviation

#Possible states of the drones
idle            = 0;
pickup          = 1;
readyfortakeoff = 2;
takeoff         = 3;
move            = 4;
readytoland     = 5;
land            = 6;
deliver         = 7;



#States of drones 31,32,33
state = np.array([idle, idle, idle]);
state1 = idle
#Initialize desired position to the base
desired_pos = np.array([ [x_base,y_base,z_base], [x_base,y_base,z_base], [x_base,y_base,z_base] ]);

#Package array
package_info = np.array([ [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0] ])
package_index = np.array([0,0,0])


#---------------------------------------------------------------------------------------------------

while(True):
    #Initialize drone status
    curr_pos = np.array([ [x_base,y_base,z_base], [x_base,y_base,z_base], [x_base,y_base,z_base] ]);
    for i in range(0,N):
        (x,y,z,battery_percentage) = status(drone_id[i])
        curr_pos[i][0]=x;
        curr_pos[i][1]=y;
        curr_pos[i][2]=z;

    i=0

    #Drone 1 is allowed to pickup parcel
    if state1 == idle:
       state1 = pickup;

    #Drone 1 picks up parcel and is ready for takeoff
    if state1 == pickup:
        for j in range(0,3):
            (x, y, z, weight, package_id) = package();
            package_info[package_index[j]][0] = x;
            package_info[package_index[j]][1] = y;
            package_info[package_index[j]][2] = z;
            package_info[package_index[j]][3] = weight;
            package_info[package_index[j]][4] = int(package_id);
        package_info[package_index[3]][0] = x_base;
        package_info[package_index[3]][1] = y_base;
        package_info[package_index[3]][2] = z_base;
        package_info[package_index[3]][3] = 0;
        package_info[package_index[3]][4] = 0;
        print(package_info)
        state1 = readyfortakeoff;

    #Drone 1 takes off
    if state1 == readyfortakeoff:
        takeoff(drone_id[i], z_takeoff, v_takeoff);
        state1 = takeoff;

    #As long as drone 1 hasn't reached z target, continue taking off
    if state1 == takeoff:
        desired_pos[i,2] = z_takeoff;
        if reached_pos(drone_id[i],desired_pos,accuracy) == 1:
            state1 = move;
            desired_pos[i,0:3]= package_info[package_index[i],0:3]

    if state1 == move:
        #call path_planning
        goto(drone_id[i],package_info[i][0] ,package_info[i][1],package_info[i][2], v_travel); 

        if reached_pos(drone_id[i],desired_pos,accuracy) == 1:
            state1 = readytoland

    if state1 == readytoland:
        land(drone_id[i],target_height,v_landing)
        state1 = landing
        des_pos[i,2] = target_height

    if state1 == landing:
        if reached_pos(drone_id[i],des_pos[i,:],accuracy) ==1:
            state1 = deliver

    if state1 == deliver:
        if deliver(drone_id[i],package_info[package_index[i]][4]) == 1:
            state1 = readyfortakeoff
            # increase package index


