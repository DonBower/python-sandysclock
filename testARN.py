#!/usr/bin/python
from ambient_api.ambientapi import AmbientAPI
import time
import json

api = AmbientAPI()

devices = api.get_devices()

device = devices[0]
print(device)

time.sleep(1) #pause for a second to avoid API limits

awnData = device.get_data()

with open('wxAWN.json','w') as jsonF:
  jsonF.write(json.dumps(awnData,indent=2,default='str'))


print('Current Temp is ' + str(awnData[0]['tempf']) + 'ºF')
# for key, value in currentData[0]:  
#   print(key + " = " + value)


# for dataset in currentData:
# with open('devices.json', 'w') as jsonF:
#     jsonF.dumps(devices, ensure_ascii=False, indent=2)

# print(str(devices))