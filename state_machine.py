import numpy as np
from util_connect import *
import time
import sys
from a_star2 import *
from obstrange import *
# -*- coding: utf-8 -*-

def reached_pos(id,des_pos,accuracy):
   (x,y,z) = status(id)
   if abs(des_pos[0]-x) <= accuracy:
       if abs(des_pos[1]-y) <= accuracy: 
           if abs(des_pos[2]-z) <= accuracy:
               print('ID: '+ str(id) +' Reached Position x:'+ str(des_pos[0]) + ' y: ' + str(des_pos[1]) + ' z: ' + str(des_pos[2]))
               return True
   else:
       return False

def reached_height(id,des_pos,accuracy):
    (x,y,z) = status(id)
    if abs(des_pos[2]-z) <= accuracy:
        print('ID: '+ str(id) + 'Reached height:'+ str(des_pos[2]))
        return True
    else:
       return False

N = 3;                              #number of drones
drone_id = np.array([31, 32, 33]);  #array containing the 3 drones' IDs
z_takeoff = 0.3;                    #takeoff altitude
v_takeoff = 0.9;                      #takeoff speed
v_travel = 0.7;                       #travel speed
v_landing = 0.1;                    #landing speed
target_height = 0;                  #landing height
goto_height = 0.1
x_base = 2.2;                       #base coordinates
y_base = 1.6;
z_base = 0;
accuracy = 0.07;                     #standard deviation

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

#Initialize desired position to the base
desired_pos = np.array([ [x_base,y_base,z_base], [x_base,y_base,z_base], [x_base,y_base,z_base] ]);

#Package array
package_info = np.array([[[x_base,y_base,0.3,0.0], [0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0]],[[x_base,y_base,0.3,0.0], [0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0]],[[x_base,y_base,0.3,0.0], [0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0]]])
package_id = [["","","",""],["","","",""],["","","",""]]
package_index = np.array([0,0,0])
counter = np.array([0,0,0])

#---------------------------------------------------------------------------------------------------
 #Initialize drone status
curr_pos = np.array([ [x_base,y_base,z_base], [x_base,y_base,z_base], [x_base,y_base,z_base] ]);
  
while(True):
    for l in range(0,N):
        (x,y,z) = status(drone_id[i])
        curr_pos[l][0]=x;
        curr_pos[l][1]=y;
        curr_pos[l][2]=z;

    for i in range(0,N):
        #Drone 1 is allowed to pickup parcel
        if state[0] == idle:
            state[0] = readyfortakeoff;
        if state[1] == idle and state[0] == pickingup:
            state[1] = readyfortakeoff;
        if state[2] == idle  and state[1] == pickingup:
            state[2] = readyfortakeoff;

        #Drone 1 picks up parcel and is ready for takeoff
        if state[i] == pickingup:
            package_index[i] = 0;
            for j in range(0,3):
                (x, y, z, weight, ids) = package();
                package_info[i][j][0] = x;
                package_info[i][j][1] = y;
                package_info[i][j][2] = z_takeoff;
                package_info[i][j][3] = weight;
                package_id[j] = ids;
                counter[i] = 0
                while(1):
                    if pickup(drone_id[i],str(ids)) == 1:
                        break
                    elif counter[i] > 8:
                        takeoff(drone_id[i], z_takeoff, v_takeoff);
                        counter[i] = counter[i] + 1
                    elif counter[i] > 20:
                        land(drone_id[i],target_height,v_landing)
                        counter[i] = counter[i] + 1
                    elif counter[i] > 50:
                        counter[i]= 0
                    counter[i] = counter[i] + 1
            package_info[i][3][0] = x_base;
            package_info[i][3][1] = y_base;
            package_info[i][3][2] = 0.3;
            package_info[i][3][3] = 0;
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
                desired_pos[i,0:3]= package_info[i,package_index[i],0:3]

        if state[i] == move:
            #call path_planning
            #x_next,y_next = call_astar(curr_pos[i][0],curr_pos[i][1],package_info[i][package_index[i]][0],package_info[i][package_index[i]][1])
            goto(drone_id[i],package_info[i][package_index[i]][0],package_info[i][package_index[i] ][1],package_info[i][package_index[i] ][2], v_travel); 
            if reached_pos(drone_id[i],desired_pos[i,:],accuracy) == 1:
                state[i] = readytoland

        if state[i] == readytoland:
            land(drone_id[i],target_height,v_landing)
            state[i] = landing
            desired_pos[i,2] = target_height

        if state[i] == landing:
            if reached_height(drone_id[i],desired_pos[i,:],0.15) ==1:
                state[i] = delivering
                counter[i] = 0

        if state[i] == delivering:
            print('ID: ' + str(i) + ' ' + package_id[package_index[i]])

            if package_info[i][package_index[i]][0] == x_base and package_info[i][package_index[i]][1] == y_base:
                state[i] = pickingup
            elif deliver(drone_id[i],str(package_id[package_index[i]])) == 1:
                state[i] = readyfortakeoff
                package_index[i] = package_index[i] + 1
            elif counter[i]>8:
                #goto(drone_id[i],package_info[i][package_index[i]][0] ,package_info[i][package_index[i] ][1],goto_height, v_travel)
                state[i] = readyfortakeoff

            counter[i] = counter[i] + 1


