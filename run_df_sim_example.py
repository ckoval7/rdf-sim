#!/usr/bin/env python3

from itertools import cycle
from time import sleep
from time import time
from bottle import route, run, request, get, post, put, response, redirect, template, static_file
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

@get('/<station_id>.xml')
def xml_out(station_id):
    if station_id == alpha.station_id:
        station = alpha
    elif station_id == bravo.station_id:
        station = bravo
    elif station_id == charlie.station_id:
        station = charlie
    else:
        return "<h3>Invalid Station ID</h3>"
    response.set_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
    output = receiver_sim.wr_xml(station.station_id, *station.current_info)
    return str(output)

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
    alpha = receiver_sim.receiver("DF_ALPHA")

    bravo = receiver_sim.receiver("DF_BRAVO")

    charlie = receiver_sim.receiver("DF_CHARLIE")
    charlie.client_url = "http://127.0.0.1:8080/position.xml"

    #Set fixed RX Location
    bravo.location = (39.253828, -76.759702)
    bravo.heading = 11

    #Use to debug tx location:
    #DOA_res_fd_tx = open("/ram/tx.xml","w")

    #Open path files for moving objects:
    #Moving RX:
    alpha.path_file = "rx_example_path.csv"
    with open(alpha.path_file, 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
        alpha.waypoints = list(reader)
    alpha.speed = 26.8 #speed m/s
    alpha.interpolated_location = receiver_sim.interpolate_all_points(alpha.waypoints, alpha.speed, resolution)

    tx = receiver_sim.transmitter()
    tx.path_file = 'tx_example_path.csv'
    #Moving TX:
    with open(tx.path_file, 'r') as file:
       reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
       tx.waypoints = list(reader)
    tx.speed = 20.12 #m/s
    tx.interpolated_location = receiver_sim.interpolate_all_points(tx.waypoints, tx.speed, resolution)
    tx_motion = cycle(tx.interpolated_location)
    rx_alpha_motion = cycle(alpha.interpolated_location)
    tx.location = next(tx_motion)
    alpha.location = next(rx_alpha_motion)
    tx.uptime = 60
    tx.downtime = 180
    next_time = round(time()) + tx.uptime

    try:
        while True:
            if round(time()) > next_time:
                tx.is_active = not tx.is_active
                delay = tx.uptime if tx.is_active == True else tx.downtime
                next_time = round(time()) + delay
                print(f"TX active: {tx.is_active}")
            alpha.next_location = next(rx_alpha_motion)
            alpha.heading = round(vincenty.get_heading(alpha.location, alpha.next_location), 1)
            tx.next_location = next(tx_motion)
            alpha.current_info = receiver_sim.rx(alpha.location, freq, tx.location, alpha.heading, tx.is_active)
            bravo.current_info = receiver_sim.rx(bravo.location, freq, tx.location, bravo.heading, tx.is_active)
            charlie.from_gps()
            charlie.current_info = receiver_sim.rx(charlie.location, freq, tx.location, charlie.heading, tx.is_active)
            alpha.location = alpha.next_location
            tx.location = tx.next_location
            sleep(resolution)

    except KeyboardInterrupt:
        finish()
