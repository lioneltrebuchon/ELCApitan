import urllib.request
import urllib3
import json
import numpy as np
import requests


hostname = 'http://10.4.14.248:5000'
register = '/api/elcapitan/register_swarm?swarm_id=elcapitan&arena_id=2&seed=12345'
connectDrone1 = '/api/elcapitan/31/connect?r=0&c=88&a=E7E7E7E731&dr=2M'
hover = '/api/test-swarm/test-drone/takeoff?z=0.5&v=0.1'
goto = '/api/test-swarm/test-drone/goto?x=1&y=1&z=0.5&yaw=0&v=0.1'
land = '/api/test-swarm/test-drone/land?z=0.0&v=0.1'
disconnect = '/api/elcapitan/31/disconnect'


result = requests.get(hostname + disconnect)
print(result.json())
#result = requests.get(hostname + connectDrone1)
#print(result.json())

