import json
import requests
import time

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
    return content

def disconnectDrone(drone_id):
    command = hostname + swarm_id + '/' + str(drone_id) + '/disconnect?dr=2M'
    r = requests.get(command)
    content = r.json()
    return content

# 5
def deliver(drone_id, package_id):
    command = hostname + swarm_id + '/' + str(drone_id) + '/deliver?dr=2M'
    r = requests.get(command)
    content = r.json()
    return content

# 6
def goto(drone_id, x, y, z, v):
    command = hostname + swarm_id + '/' + str(drone_id) + '/goto?x=' + str(x) + '&y=' + str(y) + '&z=' + str(z) + '&v=' + str(v) + '&dr=2M'
    r = requests.get(command)
    content = r.json()
    err_x = err_perc * (content['var_x'] - x)
    err_y = err_perc * (content['var_y'] - y)
    err_z = err_perc * (content['var_z'] - z)
    while( (content['var_x'] - x < err_x) and (content['var_y'] - y < err_y) and (content['var_z'] - z < err_z)):
        time.sleep(0.1)
        # Here we maybe should publish back the current position?
    # TODO here we should probably wait before returning things.
    # TODO check this!
    return (content['var_x'], content['var_y'], content['var_z'], content['battery_percentage'])

# 7
def land(drone_id):
    command = hostname + swarm_id + '/' + str(drone_id) + '/land?dr=2M'
    r = requests.get(command)
    content = r.json()
    while (content['var_z'] > 0): # TODO check this, no idea how those drones behave and wheter z = 0 is what I believe it is!
        time.sleep(0.1)
        duration = duration + 0.1
    return (content['var_x'], content['var_y'], content['var_z'], content['battery_percentage'])

# 8
def takeoff(drone_id, z, v):
    duration = 0
    command = hostname + swarm_id + '/' + str(drone_id) + '/takeoff?z=' + str(z) + '&v=' + str(v) + '&dr=2M'
    r = requests.get(command)
    content = r.json()
    err_z = err_perc * (content['var_z'] - z)
    while (content['var_z'] - z < err_z):
        time.sleep(0.1)
        duration = duration + 0.1
    return (duration, content['var_z'], content['battery_percentage'])

def getBuildings():
    command = '/api/arena'
    # Get.
    url = hostname + command
    r = urllib.request.urlopen(url).read()
    content = json.loads(r.decode('utf-8'))
    buildins = content["buildings"]
    return

# Testing.
if __name__ == "__main__":
    # Initializations.
    # hostname = 'http://10.4.14.28:5000'
    # Command to test.
    print(connectDrone(33))
    print(disconnectDrone(33))
