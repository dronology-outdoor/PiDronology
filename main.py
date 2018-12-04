import time
from os import listdir
import pixhawk
import dronekit
from simple_settings import settings

print("Onboard Dronology starting")
print("Log file: {}".format(settings.LOG_FILE))

f = open(settings.LOG_FILE, 'w')
f.write("# Start of Dronology data log:\n")

time.sleep(1)
port = pixhawk.find_devices()
if port == -1:
    print("Failed to find Pixhawk")
    f.write("Failed to find Pixhawk")
    f.close()
    import dbus
    bus = dbus.SystemBus()
    while(1):
        print("waiting")
        time.sleep(10)
    exit(-1)
f.close()

device=port[1]['pixhawks'][0][0]
print("Pixhawk found on: {}".format(device))
drone = pixhawk.connect(device)

while(1):
    data=pixhawk.get_aircraft_data(drone)
    print(data[0])
    print(data[1:])

