import pixhawk
import time 
from os import listdir
from simple_settings import settings

print (settings.LOG_FILE)
print (settings.DIR)
f=open(settings.LOG_FILE,'w')
f.write("Hello Cats\n")
f.close()

a=listdir(settings.DIR)
print("HERE")
b=listdir('./')
print(a,b)

while (1):
	print ("drones")
	time.sleep(1)
#pixhawk.hello()
#port=pixhawk.find_Devices()
#drone=pixhawk.connect(port)
#data=pixhawk.get_aircraft_data(drone)
