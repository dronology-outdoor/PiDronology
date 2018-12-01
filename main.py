import time
from os import listdir
import pixhawk
import dronekit
from simple_settings import settings

print("HERE")
print(settings.LOG_FILE)
print(settings.DIR)
f = open(settings.LOG_FILE, 'w')
f.write("Hello Frogs\n")
f.close()

print("drones")
time.sleep(1)
pixhawk.hello()
port = pixhawk.find_devices()
device=port[1]['pixhawks'][0][0]
print(device)
drone = pixhawk.connect(device)
print(str(drone.mode))

while(1)
    data=pixhawk.get_aircraft_data(drone)
    print(data[0])
    print(data[1:])

