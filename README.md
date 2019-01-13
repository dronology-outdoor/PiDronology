# PiDronology
This repo is for development with the Balena container [PiDev](https://github.com/dronology-outdoor/PiDev.git)

CURRENTLY this repo looks for a Pixhawk Autopilot connected to a USB port, requests some basic information from it if available and broadcasts that data to whoever's listing on the WLAN network.

Settings are configured in dronology_Settings.py

main.py does not attempt to listen for other devices but a simple demo reciever is provided for convinience.  

Running:
Both main and demo_recieve use simple_settings and so are executed as follows:
python main.py --settings=dronology_Settings

