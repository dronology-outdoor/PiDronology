""" Shared tool functions for interacting with the vehicle"""
import os
import subprocess
import time
import dronekit


def connect(device):
    try:
        vv = dronekit.connect(device, wait_ready=True, baud=57600)
        time.sleep(1)
        return vv
    except Exception as e:
        return (e)


def get_aircraft_data(a_vehicle):
    """Return vehicle attributes in a list"""
    utc = "0:0:0"
    lat = a_vehicle.location.global_frame.lat
    lon = a_vehicle.location.global_frame.lon
    alt = a_vehicle.location.global_frame.alt

    air_spd = a_vehicle.airspeed
    mode = str(a_vehicle.mode)
    mode = mode.split(":")[1]
    gps_stat = str(a_vehicle.gps_0)
    fix = gps_stat.split(":")[1].split(",")[0].split('=')[1]
    count = gps_stat.split(":")[1].split(",")[1].split('=')[1]

    bat_stats = str(a_vehicle.battery).split(",")
    voltage = (bat_stats[0].split("="))[-1]
    current = bat_stats[1].split("=")[-1]
    level = bat_stats[2].split("=")[-1]

    ts = time.time()
    return ["lat,lon,alt,air_spd,mode,fix,count,voltage,current,level,timestamp", lat, lon, alt, air_spd, mode, fix, count,
            voltage, current, level, ts]


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
    pixhawk_product_id = "6001"
    devices = {"k30s": [], "imets": [], "pixhawks": []}
    ports = []

    # Find all serial usb devices
    devs = os.listdir("/dev/")
    for d in devs:
        if "ttyUSB" in d:
            ports.append("/dev/" + d)
    if len(ports) == 0:
        return -1

    else:
        # Search for each product id
        for p in ports:
            po = subprocess.Popen('/sbin/udevadm info -a  --name={}'.format(p), stdout=subprocess.PIPE, shell=True)
            (output, err) = po.communicate()
            po_status = po.wait()
            output = str(output)

            if po_status == 0:
                if 'ATTRS{{idProduct}}=="{}"'.format(k30_product_id) in output:
                    # Switch on laptop vs resinOS.  5- is laptop
                    po = subprocess.Popen('/sbin/udevadm info -a  --name={} | /bin/grep \'KERNELS=="5-\''.format(p),
                                          # po = subprocess.Popen('/sbin/udevadm info -a  --name={} | /bin/grep \'KERNELS=="1-1.\''.format(p),
                                          stdout=subprocess.PIPE, shell=True)
                    (output, err) = po.communicate()
                    po.wait()

                    # Pulls kernel identification of usb port from response
                    try:
                        port_id = ids[str(output).split("\\n")[1][-2:-1]]
                    except KeyError as e:
                        # sho_logger.error("KeyError raised: {}".format(str(e)))
                        port_id = "X"
                    except IndexError as e:
                        # sho_logger.error("IndexError raised: {}".format(str(e)))
                        port_id = "X"
                    devices["k30s"].append((p, port_id))

                elif 'ATTRS{{idProduct}}=="{}"'.format(imet_product_id) in output:
                    # Switch on laptop vs resinOS.  5- is laptop
                    po = subprocess.Popen('/sbin/udevadm info -a  --name={} | /bin/grep \'KERNELS=="5-\''.format(p),
                                          # po = subprocess.Popen('/sbin/udevadm info -a  --name={} | /bin/grep \'KERNELS=="1-1.\''.format(p),
                                          stdout=subprocess.PIPE, shell=True)
                    (output, err) = po.communicate()
                    po.wait()

                    # Pulls kernel identification of usb port from response
                    try:
                        port_id = ids[str(output).split("\\n")[1][-2:-1]]
                    except KeyError as e:
                        # sho_logger.error("KeyError raised: {}".format(str(e)))
                        port_id = "X"
                    except IndexError as e:
                        # sho_logger.error("IndexError raised: {}".format(str(e)))
                        port_id = "X"
                    devices["imets"].append((p, port_id))

                elif 'ATTRS{{idProduct}}=="{}"'.format(pixhawk_product_id) in output:
                    # Switch on laptop vs resinOS.  5- is laptop
                    po = subprocess.Popen('/sbin/udevadm info -a  --name={} | /bin/grep \'KERNELS=="5-\''.format(p),
                                          # po = subprocess.Popen('/sbin/udevadm info -a  --name={} | /bin/grep \'KERNELS=="1-1.\''.format(p),
                                          stdout=subprocess.PIPE, shell=True)
                    (output, err) = po.communicate()
                    po.wait()

                    # Pulls kernel identification of usb port from response
                    try:
                        port_id = ids[str(output).split("\\n")[1][-2:-1]]
                    except KeyError as e:
                        # sho_logger.error("KeyError raised: {}".format(str(e)))
                        port_id = "X"
                    except IndexError as e:
                        # sho_logger.error("IndexError raised: {}".format(str(e)))
                        port_id = "X"
                    devices["pixhawks"].append((p, port_id))

            else:
                # sho_logger.error("Error, couldn't get udev information about ports")
                # sho_logger.info("{}".format(output.decode("utf-8")))
                # sho_logger.error(str(err))
                return -1
        return 0, devices

# a=find_devices()
# vv=connect('/dev/ttyUSB0')
# for a in range(10):
#    get_aircraft_data(vv)
# vv.close()
