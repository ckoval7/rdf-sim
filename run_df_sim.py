from itertools import cycle
from time import sleep

import csv

import receiver_sim
import mover
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

#General Variables:
resolution = 0.5 #Rate to refresh the loop, seconds
#Set TX Freq
freq = 162.4 #Arbitray

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
#alpha_lat_lon = next(rx_latlon_alpha)
alpha.speed = 26.8 #speed m/s
alpha.interpolated_location = mover.interpolate_all_points(alpha.waypoints, alpha.speed, resolution)

tx = transmitter()
tx.path_file = 'catonsville_path.csv'
#Moving TX:
with open(tx.path_file, 'r') as file:
   reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
   tx.waypoints = list(reader)
   #lat,lon
tx.speed = 20.12 #m/s
tx.interpolated_location = mover.interpolate_all_points(tx.waypoints, tx.speed, resolution)

try:
    tx_motion = cycle(tx.interpolated_location)
    rx_alpha_motion = cycle(alpha.interpolated_location)
    tx.location = next(tx_motion)
    alpha.location = next(rx_alpha_motion)
    while True:
        alpha.next_location = next(rx_alpha_motion)
        alpha.heading = round(vincenty.get_heading(alpha.location, alpha.next_location), 1)
        tx.next_location = next(tx_motion)
        receiver_sim.rx(alpha.station_id, alpha.DOA_res_fd, alpha.location, freq, tx.location, alpha.heading)
        receiver_sim.rx(bravo.station_id, bravo.DOA_res_fd, bravo.location, freq, tx.location, bravo.heading)
        #receiver_sim.wr_xml(DOA_res_fd_tx, "tx", freq, current_tx_position, 0, 0, 0, 0)
        alpha.location = alpha.next_location
        tx.location = tx.next_location
        sleep(resolution)

except KeyboardInterrupt:
    alpha.DOA_res_fd.close()
    bravo.DOA_res_fd.close()
