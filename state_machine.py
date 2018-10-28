import numpy as np
from util_connect import *
import time

# -*- coding: utf-8 -*-

def reached_pos(id,des_pos,accuracy):
   (x,y,z) = status(id)
   if abs(des_pos[0]-x) <= accuracy:
       if abs(des_pos[1]-y) <= accuracy: 
           if abs(des_pos[2]-z) <= accuracy:
               print('Reached Position x:'+ str(des_pos[0]) + ' y: ' + str(des_pos[1]) + ' z: ' + str(des_pos[2]))
               return True
   else:
       return False

def reached_height(id,des_pos,accuracy):
    (x,y,z) = status(id)
    if abs(des_pos[2]-z) <= accuracy:
        print('Reached height:'+ str(des_pos[2]))
        return True
    else:
       return False

N = 1;                              #number of drones
drone_id = np.array([32, 32, 31]);  #array containing the 3 drones' IDs
z_takeoff = 0.5;                    #takeoff altitude
v_takeoff = 0.9;                      #takeoff speed
v_travel = 0.7;                       #travel speed
v_landing = 0.1;                    #landing speed
target_height = 0;                  #landing height
x_base = 2.2;                       #base coordinates
y_base = 1.6;
z_base = 0;
accuracy = 0.03;                     #standard deviation

#Possible states of the drones
idle            = 0;
pickingup       = 1;
readyfortakeoff = 2;
takingoff       = 3;
move            = 4;
readytoland     = 5;
landing         = 6;
delivering      = 7;

reset_package(89797648235)
# connect to drone 
for i in range(0,N):
    connectDrone(drone_id[i]);

#States of drones 31,32,33
state = np.array([idle, idle, idle]);
state1 = idle
#Initialize desired position to the base
desired_pos = np.array([ [x_base,y_base,z_base], [x_base,y_base,z_base], [x_base,y_base,z_base] ]);

#Package array
package_info = np.array([ [x_base,y_base,0.5,0.0], [0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0]  ])
package_id = ["","","",""]
package_index = np.array([0,0,0])


#---------------------------------------------------------------------------------------------------
 #Initialize drone status
curr_pos = np.array([ [x_base,y_base,z_base], [x_base,y_base,z_base], [x_base,y_base,z_base] ]);
  
while(True):
    for l in range(0,N):
        (x,y,z) = status(drone_id[i])
        curr_pos[l][0]=x;
        curr_pos[l][1]=y;
        curr_pos[l][2]=z;

    i=0
    print(package_index[0])
    #Drone 1 is allowed to pickup parcel
    if state[i] == idle:
       state[i] = readyfortakeoff;

    #Drone 1 picks up parcel and is ready for takeoff
    if state[i] == pickingup:
        for j in range(0,3):
            (x, y, z, weight, ids) = package();
            package_info[j][0] = x;
            package_info[j][1] = y;
            package_info[j][2] = z_takeoff;
            package_info[j][3] = weight;
            package_id[j] = ids;
            pickup(drone_id[i],str(ids))
        package_info[3][0] = x_base;
        package_info[3][1] = y_base;
        package_info[3][2] = 0.5;
        package_info[3][3] = 0;
        package_index[i] = 0;
        print(package_info)
        print(package_id)
        state[i] = readyfortakeoff;

    #Drone 1 takes off
    if state[i] == readyfortakeoff:
        takeoff(drone_id[i], z_takeoff, v_takeoff);
        state[i] = takingoff;
        desired_pos[i,2] = z_takeoff;

    #As long as drone 1 hasn't reached z target, continue taking off
    if state[i] == takingoff:
        
        if reached_height(drone_id[i],desired_pos[i,:],accuracy) == 1:
            state[i] = move;
            desired_pos[i,0:3]= package_info[package_index[i],0:3]

    if state[i] == move:
        #call path_planning
        goto(drone_id[i],package_info[package_index[i]][0] ,package_info[package_index[i] ][1],package_info[package_index[i] ][2], v_travel); 

        if reached_pos(drone_id[i],desired_pos[i,:],accuracy) == 1:
            state[i] = readytoland

    if state[i] == readytoland:
        land(drone_id[i],target_height,v_landing)
        state[i] = landing
        desired_pos[i,2] = target_height

    if state[i] == landing:
        if reached_height(drone_id[i],desired_pos[i,:],accuracy) ==1:
            state[i] = delivering

    if state[i] == delivering:
        print(package_id[package_index[i]])

        if package_info[package_index[i]][0] == x_base and package_info[package_index[i]][1] == y_base:
            state[i] = pickingup
        elif deliver(drone_id[i],str(package_id[package_index[i]])) == 1:
            state[i] = readyfortakeoff
            package_index[i] = package_index[i] + 1
          


