import csv
import time
import math
import random
import xml.etree.ElementTree as ET

import vincenty

class receiver:
    def __init__(self, station_id):
        self.station_id = station_id

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

def wr_xml(station_id, freq, location, heading, doa, conf, pwr):
# def wr_xml(DOA_res_fd, station_id, freq, location, heading, doa, conf, pwr):
    latitude = location[0]
    longitude = location[1]
    epoch_time = int(1000 * round(time.time(), 3))
    # create the file structure
    data = ET.Element('DATA')
    xml_st_id = ET.SubElement(data, 'STATION_ID')
    xml_time = ET.SubElement(data, 'TIME')
    xml_freq = ET.SubElement(data, 'FREQUENCY')
    xml_location = ET.SubElement(data, 'LOCATION')
    xml_latitide = ET.SubElement(xml_location, 'LATITUDE')
    xml_longitude = ET.SubElement(xml_location, 'LONGITUDE')
    xml_heading = ET.SubElement(xml_location, 'HEADING')
    xml_doa = ET.SubElement(data, 'DOA')
    xml_pwr = ET.SubElement(data, 'PWR')
    xml_conf = ET.SubElement(data, 'CONF')

    xml_st_id.text = str(station_id)
    xml_time.text = str(epoch_time)
    xml_freq.text = str(freq)
    xml_latitide.text = str(round(latitude, 6))
    xml_longitude.text = str(round(longitude, 6))
    xml_heading.text = str(heading)
    xml_doa.text = str(doa)
    xml_pwr.text = str(pwr)
    xml_conf.text = str(conf)

    # create a new XML file with the results
    html_str = ET.tostring(data, encoding="unicode")
    # DOA_res_fd.seek(0)
    # DOA_res_fd.write(html_str)
    # DOA_res_fd.truncate()
    return html_str

def pathloss(distance, freq, tx_pwr = 50):
    ## TX POWER IS IN dBm!!! ##
    ## DISTANCE IS IN METERS!!! ##
    d = distance #Distance between base station and mobile station
    #Lo=8;   #Total system losses in dB
    T = 290
    BW=15*10**3; #in Hz
    #Gb=8;  #in dB
    # Gm=0;   #in dB
    # Hb=30;  #in metres
    # Hm=3.;   #in metres
    B=1.38*10**-23; #Boltzmann's constant
    # #Calculations&Results
    # Pr=Free_Lp-Lo+Gm+Gb+Pt;  #in dBW
    Te=T*(3.162-1);
    Pn=B*(Te+T)*BW;
    wavelength = freq/299.8
    path_loss = 20*math.log10((4*math.pi*d)/wavelength)
    Pr = tx_pwr - path_loss
    fudge_factor = random.randint(-10, 0)
    SNR=(Pr-10*math.log10(Pn)) + fudge_factor
    return round(SNR/2, 4)

def nosignal():
    pwr = round(random.random() + random.randint(0,3), 4)
    conf = random.randint(0,10)
    doa = random.randint(0, 359)
    return pwr, conf, doa

def rx(rx_location, freq, tx_location, heading=0, tx_active = True):
# def rx(station_id, DOA_res_fd, rx_location, freq, tx_location, heading=0, tx_active = True):
    dist_and_heading = vincenty.inverse(rx_location, tx_location)
    distance_to_target = dist_and_heading[0]
    raw_doa = dist_and_heading[1]
    pwr = pathloss(distance_to_target, freq)
    if tx_active and pwr > 1 == True:
        conf = min(int(round(0.1*pwr**2, 0)), 255)
        err_factor= 30*math.exp(-conf/8) + 3
        doa_error = int(random.triangular(-err_factor,err_factor,0))
        doa = round(doa_error + raw_doa - heading)
        if doa < 0:
            doa += 360
        elif doa > 359:
            doa -= 360
    else:
        pwr, conf, doa = nosignal()
    #Add Error:
    doa = 360 - doa #Simulates KSDR Inverted Bearing
    return freq, rx_location, heading, doa, conf, pwr
    # wr_xml(station_id, freq, rx_location, heading, doa, conf, pwr)
    # wr_xml(DOA_res_fd, station_id, freq, rx_location, heading, doa, conf, pwr)

def interpolate_two_points(coord1, coord2, speed, resolution):
    if coord1 == coord2: return coord1
    distance_and_heading = vincenty.inverse(coord1, coord2)
    distance = distance_and_heading[0]
    #print(f"Distance: {distance}")
    heading = distance_and_heading[1]
    #print(f"Heading: {heading}")
    nsteps = round(((distance/speed)*(1/resolution))/(1/resolution))/resolution
    #print(f"N Steps: {nsteps}")
    step_distance = speed*resolution
    #print(f"Step Distance: {step_distance}")
    steps = [coord1]
    current_coord = coord1
    steps_left = nsteps
    while steps_left > 0:
        #print(f"In the loop, {steps_left} to go.")
        next_coord = vincenty.direct(current_coord[0], current_coord[1], heading, step_distance)
        #print(f"Plotted: {next_coord}")
        steps.append(tuple(next_coord))
        current_coord = next_coord
        steps_left -= 1
    return steps

def interpolate_all_points(waypoints, speed, resolution):
    points_out = []
    try:
        for x in range(len(waypoints)):
            points_out.extend(interpolate_two_points(waypoints[x],  waypoints[x+1], speed, resolution))
    except IndexError:
        points_out.extend(interpolate_two_points(waypoints[-1],  waypoints[0], speed, resolution))
        return points_out


if __name__ == '__main__':
    pass
