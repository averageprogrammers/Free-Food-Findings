import json
import urllib2

def get_geometry_for_address(address):
    geometry = None
    try:
        response = urllib2.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address=" + urllib.quote(dct["location"].encode('utf-8'))
                                + "&key=AIzaSyACw_ke4ccRtwOcsqzMKL3X7WFqpR8VTtw")
        geometry = json.loads(response.read())["results"]
        #logging.info("geocoded results = %s" % geometry)
        geometry = geometry[0]["geometry"]["location"]

    except:
        print("failed to decode location while parsing event")
        print ("results = %s" % geometry)
        geometry = {"lat":0,"lng":0}
    return geometry
