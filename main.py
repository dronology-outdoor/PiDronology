import time
import pixhawk
import simple_comms as comms
from simple_settings import settings

if __name__ == "__main__":
    # TODO configure proper onboard logging
    print("Onboard Dronology starting")
    print("Log file: {}".format(settings.LOG_FILE))

    time.sleep(1)

    # Look for a pixhawk to send data from
    port = pixhawk.find_devices()
    while port == -1:
        print("{}: No pixhawk available.".format(time.ctime()))

        # Until device found alert other drones of status:
        comms.send(["No pixhawk available"], settings.BROADCAST_IP, settings.PORT)

        # Wait and look again for a pixhawk
        time.sleep(settings.PERIOD)
        port = pixhawk.find_devices()

    # Once a pixhawk is found connect to it:
    device = port[1]['pixhawks'][0][0]
    print("Pixhawk found on: {}".format(device))
    drone = pixhawk.connect(device)

    # Get data from pixhawk and broadcast to others on adhoc network
    while 1:
        data = pixhawk.get_aircraft_data(drone)
        print(time.ctime())
        print(data[0])
        print(data[1:])
        comms.send(data, settings.BROADCAST_IP, settings.PORT)
        time.sleep(settings.PERIOD)
