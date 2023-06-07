#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 17:01:51 2021

@author: Erlend Øydvin and Eivind Dalevold
"""
import requests
import pandas as pd
import datetime

# Lag din egen frost id, det er ei fil med brukernavn som streng. 
with open('/home/erlend/frost_id', 'r') as file:
    clientID = file.read().rstrip('\n')

def get_PT1M_fromid(ids, start, end):
    start = start.strftime("%Y-%m-%dT%H:%M:%S")
    end = end.strftime("%Y-%m-%dT%H:%M:%S")
    url = "https://frost.met.no/observations/v0.jsonld"
    reftime = f"{start}/{end}"
    headers = {"Accept": "application/json"}
    parameters = {
        "sources": ids,
        "referencetime": reftime,
        "elements": "sum(precipitation_amount PT1M)", #minuttnedbør
        "timeoffsets": "PT0H",
        "fields": "sourceId, referenceTime, value, elementId",
    }
    r = requests.get(url=url, params=parameters, headers=headers, auth=(clientID, ""))
    return r.json()

# laster ned måned for måned pga data begresning
start = '1968-01-01' 
stop = '2022-02-18'
time_start = datetime.datetime.strptime(start, '%Y-%m-%d')
time_stop = datetime.datetime.strptime(stop, '%Y-%m-%d')
daterange = pd.date_range(time_start, time_stop, freq='MS').tolist()
# MS: month start, M: month end

# metadata for blindern, kan legge til flere
met_stations = {
    "OSLO - BLINDERN PLU": {
        "shortname": "Blindern plu",
        "id": "SN18701",
        "name": "OSLO - BLINDERN TESTFELT",
    }  
}

for i in met_stations: 
    data = [] # array for lagring av data
    time = [] # korresponderende tid
    
    # for gjennom alle måneder siden 1968
    start = daterange[0]
    for t in daterange[1:]:
        end =  t
        r = get_PT1M_fromid(met_stations[i]["id"], start, end) # datoer overlapper ikke
        if 'error' not in r: # mulig snø på vinteren, denne hopper over intervaller med manglende nedbør
            print("downloading: ", start.strftime("%Y-%m"))
            for j in r['data']:
                data.append(j['observations'][0]['value'])
                time.append( j['referenceTime'] )
        else:
            print("skip: ", start.strftime("%Y-%m"))
        start = end
        
    
    df = pd.DataFrame(data={'time':time, 'PT1H':data})
    df = df.set_index('time')
    df.to_csv('./Blindern_PT1M')

    

#df[14350:14390]





