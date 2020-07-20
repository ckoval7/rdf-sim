from lxml import etree
from time import sleep
import simplekml

url_a = "/ram/DF_ALPHA.xml"
url_b = "/ram/DF_BRAVO.xml"
url_tx = "/ram/tx.xml"

kml = simplekml.Kml()

def start_logging(url):
    try:
        xml_contents = etree.parse(url)
        location = []
        xml_station_id = xml_contents.find('STATION_ID')
        station_id = xml_station_id.text
        xml_latitude = xml_contents.find('LOCATION/LATITUDE')
        location.append(float(xml_latitude.text))
        xml_longitude = xml_contents.find('LOCATION/LONGITUDE')
        location.append(float(xml_longitude.text))
        xml_heading = xml_contents.find('LOCATION/HEADING')
        heading = xml_heading.text
        path_list = (float(xml_longitude.text),float(xml_latitude.text))
        return path_list

    except OSError:
        print("File doesn't exist!")
        time.sleep(1)

def finish_logging(filename, foldername, path):
    fol = kml.newfolder()
    fol.name = foldername
    fol.description = foldername + " Path"
    style = simplekml.Style()
    style.iconstyle.scale = 0.5
    style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/grn-blank-lv.png'
    ls.coords = path
    ls.extrude = 1
    ls.altitudemode = simplekml.AltitudeMode.clamptoground
    ls.style.linestyle.width = 5
    ls.style.linestyle.color = simplekml.Color.blue
    kml.save(filename)

if __name__ == '__main__':
    try:
        rx_path = []
        tx_path = []
        while True:
            #rx_path.append(start_logging(url_a))
            tx_path.append(start_logging(url_tx))
            sleep(1)
    except KeyboardInterrupt:
        ls = kml.newlinestring(name='Path')
        #finish_logging("rx1.kml", "RX Path", rx_path)
        finish_logging("tx1.kml", "TX Path", tx_path)
