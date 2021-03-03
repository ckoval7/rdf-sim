#!/usr/bin/env python3

from itertools import cycle
from random import randint
from time import sleep, time
from bottle import route, run, request, get, response, redirect, template, static_file
from optparse import OptionParser
from os import system, name, kill, getpid

import signal,sys
import csv
import threading

import receiver_sim
import vincenty

@route('/static/<filepath:path>', name='static')
def server_static(filepath):
    response = static_file(filepath, root='./static')
    response.set_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
    return response

@get('/')
@get('/home')
@get('/index.html')
def home():
    return template('index.tpl')

def start_server(ipaddr = "127.0.0.1", port=8081):
    try:
        run(host=ipaddr, port=port, quiet=True, server="paste", debug=True)
    except OSError:
        print(f"Port {port} seems to be in use. Please select another port or " +
        "check if another instance of rdf-sim is already running.")
        finish()

def finish():
    print("\nDying, please wait.")
    kill(getpid(), signal.SIGTERM)

@get('/<station_id>.xml')
def xml_out(station_id):
    response.set_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
    for x in receivers:
        if station_id == x.station_id:
            return str(receiver_sim.wr_xml(x.station_id, *x.current_info))
        else:
            return "<h3>Invalid Station ID</h3>"

receivers = []
transmitters = []

if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("--ip", dest="ipaddr", help="IP Address to serve from. Default 127.0.0.1",
    metavar="IP ADDRESS", type="str", default="127.0.0.1")
    parser.add_option("--port", dest="port", help="Port number to serve from. Default 8081",
    metavar="NUMBER", type="int", default=8081)
    (options, args) = parser.parse_args()

    web = threading.Thread(target=start_server,args=(options.ipaddr, options.port))
    web.daemon = True
    web.start()

    #General Variables:
    resolution = 0.5 #Rate to refresh the loop, seconds
    #Set TX Freq
    freq = 162.4 #Arbitrary

    #Name DF Stations
    receivers.append(receiver_sim.receiver("DF_ALPHA"))
    receivers[-1].path_file = "rx_example_path.csv"
      with open(receivers[-1].path_file, 'r') as file:
          reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
          receivers[-1].waypoints = list(reader)
      receivers[-1].speed = 26.8 #speed m/s
      receivers[-1].interpolated_location = receiver_sim.interpolate_all_points(receivers[-1].waypoints, receivers[-1].speed, resolution)
      rx_receivers[-1]_motion = cycle(receivers[-1].interpolated_location)
      receivers[-1].location = next(rx_receivers[-1]_motion)
    # alpha = receivers[-1]

    receivers.append(receiver_sim.receiver("DF_BRAVO"))
    receivers[-1].location = (39.253828, -76.759702)
    receivers[-1].heading = 11
    # bravo = receivers[-1]

    receivers.append(receiver_sim.receiver("DF_CHARLIE"))
    receivers[-1].client_url = "http://127.0.0.1:8080/position.xml"
    # charlie = receivers[-1]

    transmitters.append(receiver_sim.transmitter())
    #Moving TX:
    transmitters[-1].path_file = 'tx_example_path.csv'
    with open(transmitters[-1].path_file, 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
        transmitters[-1].waypoints = list(reader)
    transmitters[-1].speed = 20.12 #m/s
    transmitters[-1].interpolated_location = receiver_sim.interpolate_all_points(transmitters[-1].waypoints, transmitters[-1].speed, resolution)
    tx_motion = cycle(transmitters[-1].interpolated_location)
    transmitters[-1].location = next(tx_motion)
    transmitters[-1].uptime = 60
    transmitters[-1].downtime = 180
    tx = transmitters[-1]

    try:
        next_time = round(time()) + tx.uptime
        while True:
            if round(time()) > next_time:
                tx.is_active = not tx.is_active
                delay = tx.uptime if tx.is_active == True else tx.downtime
                next_time = round(time()) + delay
                print(f"TX active: {tx.is_active}")
            alpha.next_location = next(rx_alpha_motion)
            alpha.heading = round(vincenty.get_heading(alpha.location, alpha.next_location), 1)
            tx.next_location = next(tx_motion)
            charlie.from_gps()

            for rx in receivers:
                rx.current_info = receiver_sim.rx(rx.location, freq, tx.location, rx.heading, tx.is_active)\

            alpha.location = alpha.next_location
            tx.location = tx.next_location
            sleep(resolution)

    except KeyboardInterrupt:
        finish()
