#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 13:47:42 2022

@author: Erlend Øydvin and Eivind Dalevold
"""

import requests
import pickle
import datetime

# get client ID
with open('/home/erlend/frost_id', 'r') as file:
    clientID = file.read().rstrip('\n')

def get_available_gauges_in_area(geometry=None, elements=None, 
                                 validtime = None, country = None):
    url = "https://frost.met.no/sources/v0.jsonld"
    headers = {"Accept": "application/json", "Authorization": f"Basic {clientID}"}
    params = {
        "types": "SensorSystem",
        "geometry": geometry,
        "elements": elements,
        "validtime": validtime,
        "country": country,
    }
    r = requests.get(url, params, headers=headers, auth=(clientID, ""))
    return r.json()


# Geometry specifications: 
# https://frost.met.no/concepts2.html#geometryspecification

# Get available stations in box:
# http://bboxfinder.com/#59.570506,10.517349,59.790616,10.962982

bbox = [1.845703,57.680660,14.897461,63.801894] #norge sør for Steinkjer ish
country = 'Norge' # set to none to include ie sweden
# Type element
elements = "sum(precipitation_amount PT1M)"  #timesnedbør
#elements = "sum(precipitation_amount PT1M)" #minuttnedbør

# Valid timeinterval
#start = '2018-08-07' 
#end = '2018-08-09'

start = '1960-01-01' 
end = '2021-01-01'


if (start is not None) and (end is not None):
    validtime = f"{start}/{end}"
elif (end is None) and (start is not None):
    validtime = f"{start}"
else: # all times included
    validtime = None

# bbox to polygon
a = str(bbox[0]) + " " + str(bbox[1])
b = str(bbox[2]) + " " + str(bbox[1])
c = str(bbox[2]) + " " + str(bbox[3])
d = str(bbox[0]) + " " + str(bbox[3])
geomet = "POLYGON((" + a + ", " + b + ", " + c + ", " + d + "))"



s = get_available_gauges_in_area(geometry=geomet, 
                                 elements = elements,
                                 validtime = validtime,
                                 country = country,
                                 )

metadata = {}
for station in s['data']:
    metadata[station['name']] = {
        "shortname": station['shortName'],
        "id": station['id'],
        "name": station['name'],
        "resolution": str(elements), 
        "lat": station['geometry']['coordinates'][1],
        "lon": station['geometry']['coordinates'][0]
        }

a_file = open("./meta_data.pkl", "wb")
pickle.dump(metadata, a_file)
a_file.close()
