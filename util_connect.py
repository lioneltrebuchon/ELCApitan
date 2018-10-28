import json
import requests
import time
import numpy

# Initializations
channel = '88'
address = 'E7E7E7E7'
radio = '0'
swarm_id = 'elcapitan'
hostname = 'http://10.4.14.248:5000/api/'
mode = 'urllib3'
err_perc = 0.1

# Functions

def createSwarmID():
    swarm_id = 'elcapitan'
    command = hostname + swarm_id + '/register_swarm?arena_id=2'
    r = requests.get(command)
    content = r.json()
    return content

def connectDrone(drone_id):
    addressDrone = address + str(drone_id)
    command = hostname + swarm_id + '/' + str(drone_id) + '/connect?r=' + radio + '&c=' + channel + '&a=' + addressDrone + '&dr=2M'
    r = requests.get(command)
    content = r.json()
    print(content)
    x = content['x']
    y = content['y']
    z = content['z']
    #battery_percentage = content['battery_percentage']
    return (x,y,z)#battery_percentage)
    

def disconnectDrone(drone_id):
    command = hostname + swarm_id + '/' + str(drone_id) + '/disconnect?dr=2M'
    r = requests.get(command)
    content = r.json()
    return content

def status(drone_id):
    command = hostname + swarm_id + '/' + str(drone_id) + '/status?dr=2M'
    r = requests.get(command)
    content = r.json()
    id = content['id']
    x = content['x']
    y = content['y']
    z = content['z']
    #battery_percentage = content['battery_percentage']
    return (x,y,z)

def package():
    command = hostname + swarm_id + '/package?dr=2M'
    r = requests.get(command)
    content = r.json()
    print(content)
    coordinates = numpy.array(content['coordinates'])
    x = coordinates[0]
    y = coordinates[1]
    z = coordinates[2]
    id = content['id']
    weight = content['weight']
    return (x,y,z, weight, id)

def pickup(drone_id, package_id):
    command = hostname + swarm_id + '/' + str(drone_id) + '/pickup?dr=2M&package_id=' + str(package_id)
    r = requests.get(command)
    content = r.json()
    print(content)
    return content['success']

def reset_package( seed):
    command = hostname + swarm_id + '/reset_package_generator?dr=2M&swarm_id=' + str(swarm_id)
    r = requests.get(command)
    content = r.json()
    print(content)
    return content['success']

# 5
def deliver(drone_id, package_id):
    command = hostname + swarm_id + '/' + str(drone_id) + '/deliver?dr=2M&package_id=' + str(package_id)
    r = requests.get(command)
    content = r.json()
    print(content)
    return content['success']

# 6
def goto(drone_id, x, y, z, v):
    command = hostname + swarm_id + '/' + str(drone_id) + '/goto?x=' + str(x) + '&y=' + str(y) + '&z=' + str(z) + '&v=' + str(v) + '&dr=2M'
    r = requests.get(command)
    content = r.json()
    print(content)
    return content['duration']

# 7
def land(drone_id,target_height,vel):
    command = hostname + swarm_id + '/' + str(drone_id) + '/land?dr=2M&z=' + str(target_height) + '&v=' + str(vel)
    r = requests.get(command)
    content = r.json()
    print(content)
    #while (content['var_z'] > 0): # TODO check this, no idea how those drones behave and wheter z = 0 is what I believe it is!
    #    time.sleep(0.1)
    #    duration = duration + 0.1
    return content['duration']

# 8
def takeoff(drone_id, z, v):
    duration = 0
    command = hostname + swarm_id + '/' + str(drone_id) + '/takeoff?z=' + str(z) + '&v=' + str(v) + '&dr=2M'
    r = requests.get(command)
    content = r.json()
    print( content)
    return content['duration']

def getBuildings():
    command = '/api/arena'
    # Get.
    url = hostname + command
    r = urllib.request.urlopen(url).read()
    content = json.loads(r.decode('utf-8'))
    buildins = content["buildings"]
    return


# Testing.
#if __name__ == "__main__":
    # Initializations.
    # hostname = 'http://10.4.14.28:5000'
    # Command to test.
    #(x,y,z,weight, id) = package()
    #print(status(31))

    connectDrone(31)
    (x,y,z, weight, id) = package()
    wait = takeoff(31,0.5,1)
    time.sleep(wait)
    wait = goto(31,x,y,z,0.5)
    time.sleep(wait)
    wait = land(31,0,0.2)
    time.sleep(wait)

    
    deliver(31,id)
    time.sleep(2)
    disconnectDrone(31)

