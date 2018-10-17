""" Shared tool functions for interacting with the vehicle"""
import os
import sys
import time
from dronekit import connect

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

vv=connect()
f=open('/data/mydata','rw')
for i in range(10):
	data=get_aircraft_data(vv)
	f.write()
f.close()



