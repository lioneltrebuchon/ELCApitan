import urllib.request
import json
import requests
import numpy

# Initializations
channel = '88'
address = 'E7E7E7E7'
radio = '0'
swarm_id = 'elcapitan'

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


def goto():
    return 0

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
    hostname = 'http://10.4.14.248:5000/api/'
    mode = 'urllib3'
    # Command to test.
    print(connectDrone(33))
    print(disconnectDrone(33))
