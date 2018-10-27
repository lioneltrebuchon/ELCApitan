import urllib.request
import json
import numpy

# Initializations.
hostname = 'http://10.4.14.28:5000'
command = '/api/arena'
mode = 'urllib3'

# Get.
url = hostname + command
r = urllib.request.urlopen(url).read()
content = json.loads(r.decode('utf-8'))

print(content)

# Set. TODO