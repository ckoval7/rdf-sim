#!/usr/bin/env python3

from bottle import run, request, get, response
from os import system, name, kill, getpid
from optparse import OptionParser
import threading
import signal
import xml.etree.ElementTree as ET
import gpsd
import time

gpsd.connect()

def start_server(ipaddr = "0.0.0.0", port=8080):
    try:
        run(host=ipaddr, port=port, quiet=True, server="paste", debug=True)
    except OSError:
        print(f"Port {port} seems to be in use. Please select another port or " +
        "check if another instance of %prog is already running.")
        finish()

def finish():
    print("\nDying, please wait.")
    kill(getpid(), signal.SIGTERM)

@get('/position.xml')
def postion():
    response.set_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
    return wr_xml()

def wr_xml():
    try:
        packet = gpsd.get_current()
        latitude, longitude = packet.position()
        heading = packet.movement().get('track')
    except (gpsd.NoFixError, UserWarning):
        latitude = longitude = 0.0
        heading = 0

    data = ET.Element('DATA')
    xml_st_id = ET.SubElement(data, 'STATION_ID')
    xml_latitide = ET.SubElement(data, 'LATITUDE')
    xml_longitude = ET.SubElement(data, 'LONGITUDE')
    xml_heading = ET.SubElement(data, 'HEADING')
    xml_st_id.text = str(station_id)
    xml_latitide.text = str(latitude)
    xml_longitude.text = str(longitude)
    xml_heading.text = str(heading)

    return ET.tostring(data, encoding="unicode")
    #print("Wrote XML")

def clear(debugging):
    if not debugging:
        # for windows
        if name == 'nt':
            _ = system('cls')
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')

def finish():
    print("\nDying, please wait.")
    kill(getpid(), signal.SIGTERM)

if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-s", "--station_id", dest="station_id", help="The name of this station",
    metavar="string", type="str", default="MyStation")
    parser.add_option("--ip", dest="ipaddr", help="IP Address to serve from. Default 0.0.0.0",
    metavar="IP ADDRESS", type="str", default="0.0.0.0")
    parser.add_option("--port", dest="port", help="Port number to serve from. Default 8080",
    metavar="NUMBER", type="int", default=8080)
    parser.add_option("--debug", dest="debugging", help="Does not clear the screen. Useful for seeing errors and warnings.",
    action="store_true")
    (options, args) = parser.parse_args()

    debugging = False if not options.debugging else True

    web = threading.Thread(target=start_server,args=(options.ipaddr, options.port))
    web.daemon = True
    web.start()

    station_id = options.station_id

    try:
        dots = 0
        while(True):
            time.sleep(1)
            clear(debugging)
            if dots > 5:
                dots = 1
            else:
                dots += 1
            print("Running" + dots*'.')
            print("Press Control+C to exit.")

    except KeyboardInterrupt:
        finish()
