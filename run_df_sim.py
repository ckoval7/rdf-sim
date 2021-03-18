#!/usr/bin/env python3

from itertools import cycle
from random import randint
from time import sleep, time
from bottle import route, run, request, get, response, redirect, template, static_file
from optparse import OptionParser
from os import system, name, kill, getpid

import signal,sys
import csv, json
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
    rx_ids = []
    for id in receivers:
        rx_ids.append(id.station_id)
    return template('index.tpl', {'rx_ids': rx_ids})

@get('/<station_id>.xml')
def xml_out(station_id):
    response.set_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
    for x in receivers:
        if station_id == x.station_id:
            return str(receiver_sim.wr_xml(x.station_id, *x.current_info))

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

receivers = []
transmitters = []

if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-j", "--json", dest="json_file", help="REQUIRED JSON File", metavar="FILE")
    parser.add_option("--ip", dest="ipaddr", help="IP Address to serve from. Default 127.0.0.1",
    metavar="IP ADDRESS", type="str", default="127.0.0.1")
    parser.add_option("--port", dest="port", help="Port number to serve from. Default 8081",
    metavar="NUMBER", type="int", default=8081)
    (options, args) = parser.parse_args()

    mandatories = ['json_file']
    for m in mandatories:
      if options.__dict__[m] is None:
        print("You forgot an arguement")
        parser.print_help()
        exit(-1)

    event_info = json.load(open(options.json_file,))

    web = threading.Thread(target=start_server,args=(options.ipaddr, options.port))
    web.daemon = True
    web.start()

    #General Variables:
    resolution = 0.5 #Rate to refresh the loop, seconds
    #Set TX Freq
    freq = float(event_info['scenario']['frequency'])

    #DF Stations
    for rx in event_info['scenario']['receivers']:
        receivers.append(receiver_sim.receiver(rx['station_id']))
        receivers[-1].movement_type = rx['rx_type']
        if rx['rx_type'] == "stationary":
            receivers[-1].location = (float(rx['latitude']), float(rx['longitude']))
            receivers[-1].heading = float(rx['heading'])

        elif rx['rx_type'] == "mobile":
            receivers[-1].path_file = rx['pathfile']
            with open(receivers[-1].path_file, 'r') as file:
                reader = list(csv.reader(file, quoting=csv.QUOTE_NONNUMERIC))
                if reader[0] == reader[-1]:
                    reader.pop(-1)
                # print(f"Number of waypoints: {len(reader)}")
                receivers[-1].waypoints = reader
            receivers[-1].speed = float(rx['speed']) #speed m/s
            receivers[-1].interpolated_location = receiver_sim.interpolate_all_points(receivers[-1].waypoints, receivers[-1].speed, resolution)
            receivers[-1].motion = cycle(receivers[-1].interpolated_location)
            receivers[-1].location = next(receivers[-1].motion)
            # print(f"Mobile RX start Location: {receivers[-1].location}")

        elif rx['rx_type'] == "gps":
            receivers[-1].client_url = rx['gpsAddr']

    for tx in event_info['scenario']['transmitters']:
        transmitters.append(receiver_sim.transmitter())
        transmitters[-1].id = tx['tx_id']
        transmitters[-1].movement_type = tx['tx_type']
        transmitters[-1].uptime = lambda : randint(int(tx['minUptime']), int(tx['maxUptime']))
        transmitters[-1].downtime = lambda : randint(int(tx['minDowntime']), int(tx['maxDowntime']))
        if tx['tx_type'] == "stationary":
            transmitters[-1].location = (float(tx['latitude']), float(tx['longitude']))

        elif tx['tx_type'] == "mobile":
            transmitters[-1].path_file = tx['pathfile']
            with open(transmitters[-1].path_file, 'r') as file:
                reader = list(csv.reader(file, quoting=csv.QUOTE_NONNUMERIC))
                if reader[0] == reader[-1]:
                    reader.pop(-1)
                transmitters[-1].waypoints = reader
            transmitters[-1].speed = float(tx['speed']) #speed m/s
            transmitters[-1].interpolated_location = receiver_sim.interpolate_all_points(transmitters[-1].waypoints, transmitters[-1].speed, resolution)
            transmitters[-1].motion = cycle(transmitters[-1].interpolated_location)
            transmitters[-1].location = next(transmitters[-1].motion)

        elif tx['tx_type'] == "gps":
            transmitters[-1].client_url = tx['gpsAddr']

    try:
        tx_order = event_info['scenario']['txOrder']
        if tx_order == "random":
            next_tx = lambda : transmitters[randint(0, len(transmitters)-1)]
        else:
            tx_cyc = cycle(transmitters)
            next_tx = lambda : next(tx_cyc)

        current_tx = next_tx()
        current_tx.is_active = True
        delay = current_tx.uptime()
        next_time = round(time()) + delay
        print(f"TX {current_tx.id} will be active for {delay}s")
        while True:
            if round(time()) >= next_time:
                if current_tx.is_active:
                    current_tx.is_active = False #Make it inactive
                    delay = current_tx.downtime()
                    next_time = round(time()) + delay #Wait for downtime
                    print(f"Transmitters will sleep for {delay}s")
                else:
                    current_tx = next_tx() #Move to the next TX
                    delay = current_tx.uptime()
                    next_time = round(time()) + delay #Set uptime
                    current_tx.is_active = True #Make it active
                    print(f"TX {current_tx.id} will be active for {delay}s")

            for txs in transmitters:
                if txs.movement_type == "mobile":
                    txs.location = next(txs.motion)
                elif txs.movement_type == "gps":
                    txs.from_gps()

            for rx in receivers:
                if rx.movement_type == "mobile":
                    rx.next_location = next(rx.motion)
                    rx.heading = round(vincenty.get_heading(rx.location, rx.next_location), 1)
                    rx.location = rx.next_location
                elif rx.movement_type == "gps":
                    rx.from_gps()
                # print(rx.location, freq, current_tx.location, rx.heading, current_tx.is_active)
                rx.current_info = receiver_sim.rx(rx.location, freq, current_tx.location, rx.heading, current_tx.is_active)

            sleep(resolution)

    except KeyboardInterrupt:
        finish()
