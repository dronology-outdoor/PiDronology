""" Shared tool functions for interacting with the vehicle"""
import os
import sys
import time
from dronekit import connect
import datetime
import serial

def hello():
	print("fred")

def connect(device):
    try:
        vv = connect(device, wait_ready=True, baud=57600)
        return (vv,0)
    except Exception as e:
        return (e)

def get_aircraft_data(aVehicle):
    """Return vehicle attributes in a list"""
    utc = "0:0:0"
    lat = aVehicle.location.global_frame.lat
    long = aVehicle.location.global_frame.lon
    alt = aVehicle.location.global_frame.alt

    air_spd = aVehicle.airspeed
    mode = str(aVehicle.mode)
    mode=mode.split(":")[1]
    gps_stat = str(aVehicle.gps_0)
    fix = gps_stat.split(":")[1].split(",")[0].split('=')[1]
    count = gps_stat.split(":")[1].split(",")[1].split('=')[1]

    bat_stats = str(aVehicle.battery).split(",")
    voltage = (bat_stats[0].split("="))[-1]
    current = bat_stats[1].split("=")[-1]
    level = bat_stats[2].split("=")[-1]

    id = time.time()
    return [lat,long,alt,air_spd,mode,fix,count,voltage,current,level,id]

vv=connect('/dev/ttyUSB0')
get_aircraft_data(vv)

def find_devices():
    """
    Find available serial device sensors
    :return:Dictionary of devices in type lists of tuples (<path>,<id>)
    devices = {'k30s': [('/dev/ttyUSB1', 'A')], 'imets': [], 'pixhawks': []}
    """
    # Ids of USB ports found on a Pi3B+  possible differs on other devices
    ids = {"2": "A", "4": "B", "3": "C", "5": "D"}
    k30_product_id = "ea60"
    imet_product_id = "6015"
    # TODO get actual Pixhawk product ID and add to search
    #TODO new means of identifying I2C CO2meters
    pixhawk_product_id = "BEEF"
    devices = {"k30s": [], "imets": [], "pixhawks": []}
    ports = []

    # Find all serial usb devices
    devs = os.listdir("/dev/")
    for d in devs:
        if "ttyUSB" in d:
            ports.append("/dev/" + d)

    # Search for each product id
    for p in ports:
        po = subprocess.Popen('/sbin/udevadm info -a  --name={}'.format(p), stdout=subprocess.PIPE, shell=True)
        (output, err) = po.communicate()
        po_status = po.wait()
        output = str(output)

        if po_status == 0:
            if 'ATTRS{{idProduct}}=="{}"'.format(k30_product_id) in output:
                po = subprocess.Popen('/sbin/udevadm info -a  --name={} | /bin/grep \'KERNELS=="1.\''.format(p),
                                      stdout=subprocess.PIPE, shell=True)
                (output, err) = po.communicate()
                po.wait()

                # Pulls kernel identification of usb port from response
                try:
                    port_id = ids[str(output).split("\\n")[1][-2:-1]]
                except KeyError as e:
                    sho_logger.error("KeyError raised: {}".format(str(e)))
                    port_id = "X"
                except IndexError as e:
                    sho_logger.error("IndexError raised: {}".format(str(e)))
                    port_id = "X"
                devices["k30s"].append((p, port_id))

            elif 'ATTRS{{idProduct}}=="{}"'.format(imet_product_id) in output:
                po = subprocess.Popen('/sbin/udevadm info -a  --name={} | /bin/grep \'KERNELS=="1.\''.format(p),
                                      stdout=subprocess.PIPE, shell=True)
                (output, err) = po.communicate()
                po.wait()

                # Pulls kernel identification of usb port from response
                try:
                    port_id = ids[str(output).split("\\n")[1][-2:-1]]
                except KeyError as e:
                    sho_logger.error("KeyError raised: {}".format(str(e)))
                    port_id = "X"
                except IndexError as e:
                    sho_logger.error("IndexError raised: {}".format(str(e)))
                    port_id = "X"
                devices["imets"].append((p, port_id))

            elif 'ATTRS{{idProduct}}=="{}"'.format(pixhawk_product_id) in output:
                po = subprocess.Popen('/sbin/udevadm info -a  --name={} | /bin/grep \'KERNELS=="1.\''.format(p),
                                      stdout=subprocess.PIPE, shell=True)
                (output, err) = po.communicate()
                po.wait()

                # Pulls kernel identification of usb port from response
                try:
                    port_id = ids[str(output).split("\\n")[1][-2:-1]]
                except KeyError as e:
                    sho_logger.error("KeyError raised: {}".format(str(e)))
                    port_id = "X"
                except IndexError as e:
                    sho_logger.error("IndexError raised: {}".format(str(e)))
                    port_id = "X"
                devices["pixhawks"].append((p, port_id))

        else:
            sho_logger.error("Error, couldn't get udev information about ports")
            sho_logger.info("{}".format(output.decode("utf-8")))
            sho_logger.error(str(err))
            return -1
    sho_logger.info("Devices found: {}".format(devices))
    return 0, devices
