#!/usr/bin/env python3

from os import system, name, kill, getpid
from bottle import route, run, request, get, response, redirect, template, static_file
import signal,sys
import threading

imports = """#!/usr/bin/env python3

# This file was generated using the scenario generator

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
"""

webserver = """
@route('/static/<filepath:path>', name='static')
def server_static(filepath):
    response = static_file(filepath, root='./static')
    response.set_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
    return response

# @get('/')
# @get('/home')
# @get('/index.html')
# def home():
# # Set up a home page for your scenario
#     return template('index.tpl')

@get('/<station_id>.xml')
def xml_out(station_id):
    response.set_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
    for x in receivers:
        if station_id == x.station_id:
            return str(receiver_sim.wr_xml(x.station_id, *x.current_info))
        else:
            return "<h3>Invalid Station ID</h3>"

def start_server(ipaddr = "127.0.0.1", port=8081):
    try:
        run(host=ipaddr, port=port, quiet=True, server="paste", debug=True)
    except OSError:
        print(f"Port {port} seems to be in use. Please select another port or " +
        "check if another instance of rdf-sim is already running.")
        finish()
"""

finisher = """
def finish():
    print("\nDying, please wait.")
    kill(getpid(), signal.SIGTERM)
"""

top_of_main = """
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
"""

def random_updown(var_name, low, high):
    return f"randint({low}, {high})"

def set_globals(frequency, resolution):
    return f"""
    receivers = []
    transmitters = []
    frequency = {frequency}
    resolution = {resolution}
    """

def create_moving_rx(path, speed):
    return f"""
    receivers[-1].path_file = '{path}'

    with open(receivers[-1].path_file, 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
        receivers[-1].waypoints = list(reader)

    receivers[-1].speed = {speed} #speed m/s
    receivers[-1].interpolated_location = receiver_sim.interpolate_all_points(receivers[-1].waypoints, receivers[-1].speed, resolution)
    receivers[-1].motion = cycle(receivers[-1].interpolated_location)
    receivers[-1].location = next(receivers[-1].motion)
    """

def create_stationary_rx(latitude, longitude, heading):
    return f"""
    receivers[-1].location = ({latitude}, {longitude})
    receivers[-1].heading = {heading}
    """

def create_gps_rx(url):
    return f"""
    receivers[-1].client_url = '{url}'
    """

def create_moving_tx(path, speed, uptime, downtime):
    return f"""
    transmitters[-1].path_file = '{path}'

    with open(transmitters[-1].path_file, 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
        transmitters[-1].waypoints = list(reader)

    transmitters[-1].speed = {speed} #m/s
    transmitters[-1].interpolated_location = receiver_sim.interpolate_all_points(transmitters[-1].waypoints, transmitters[-1].speed, resolution)
    transmitters[-1].motion = cycle(transmitters[-1].interpolated_location)
    transmitters[-1].location = next(transmitters[-1].motion)
    transmitters[-1].uptime = lambda: {uptime}
    transmitters[-1].downtime = lambda: {downtime}
    """

def create_stationary_tx(latitude, longitude, uptime, downtime):
    return f"""
    transmitters[-1].location = ({latitude}, {longitude})
    transmitters[-1].uptime = lambda: {uptime}
    transmitters[-1].downtime = lambda: {downtime}
    """

def create_gps_tx(url, uptime, downtime):
    return f"""
    transmitters[-1].client_url = '{url}'
    transmitters[-1].uptime = lambda: {uptime}
    transmitters[-1].downtime = lambda: {downtime}
    """

@route('/static/<filepath:path>', name='static')
def server_static(filepath):
    response = static_file(filepath, root='./static')
    response.set_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
    return response

@get('/')
@get('/scenario_generator')
def home():
    return template('scenario_generator.tpl')

def start_server(ipaddr = "127.0.0.1", port=8080):
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
    parser.add_option("--port", dest="port", help="Port number to serve from. Default 8080",
    metavar="NUMBER", type="int", default=8080)
    (options, args) = parser.parse_args()

    web = threading.Thread(target=start_server,args=(options.ipaddr, options.port))
    web.daemon = True
    web.start()
