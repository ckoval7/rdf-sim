from itertools import cycle
from time import sleep
from time import time

import csv

import receiver_sim
import vincenty

class receiver:
    def __init__(self, station_id):
        self.station_id = station_id
        #If Station IDs contain /, use this
        self.outfile = station_id.replace("/","")
        #Allows for the station ID to have a /, but removes it from the filename.
        self.DOA_res_fd = open("/ram/" + self.outfile + ".xml","w")
    heading = 0
    speed = 0
    location = ()
    next_location = ()
    path_file = ""
    waypoints = []
    interpolated_location = []

class transmitter:
    heading = 0
    speed = 0
    location = ()
    next_location = ()
    path_file = ""
    waypoints = []
    interpolated_location = []
    is_active = True
    uptime = 0
    downtime = 0

#General Variables:
resolution = 0.5 #Rate to refresh the loop, seconds
#Set TX Freq
freq = 162.4 #Arbitrary

#Name DF Stations
alpha = receiver("DF_ALPHA")

bravo = receiver("DF_BRAVO")

#Set fixed RX Location
bravo.location = (39.253828, -76.759702)
bravo.heading = 11

#Use to debug tx location:
#DOA_res_fd_tx = open("/ram/tx.xml","w")

#Open path files for moving objects:
#Moving RX:
alpha.path_file = "path.csv"
with open(alpha.path_file, 'r') as file:
    reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
    alpha.waypoints = list(reader)
alpha.speed = 26.8 #speed m/s
alpha.interpolated_location = receiver_sim.interpolate_all_points(alpha.waypoints, alpha.speed, resolution)

tx = transmitter()
tx.path_file = 'catonsville_path.csv'
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
        receiver_sim.rx(alpha.station_id, alpha.DOA_res_fd, alpha.location, freq, tx.location, alpha.heading, tx.is_active)
        receiver_sim.rx(bravo.station_id, bravo.DOA_res_fd, bravo.location, freq, tx.location, bravo.heading, tx.is_active)
        #receiver_sim.wr_xml(DOA_res_fd_tx, "tx", freq, tx.location, 0, 0, 0, 0)
        alpha.location = alpha.next_location
        tx.location = tx.next_location
        sleep(resolution)

except KeyboardInterrupt:
    alpha.DOA_res_fd.close()
    bravo.DOA_res_fd.close()
