from GetResult import GetResult
import requests  # Import the requests library
import pandas as pd
import xml.etree.ElementTree as ET
from time import gmtime, strftime
from datetime import datetime
import time
from pytz import timezone,utc
import pprint
import json
import numpy as np

def BusCheckOutbound(BusNumber):

  input = BusNumber

  address = 'https://data.etabus.gov.hk/v1/transport/kmb/route-stop/'+input+'/outbound/1'

  payload = GetResult(address)  #inbound

  bus_dataset = pd.DataFrame(payload['data'], columns=['bound', 'route', 'seq', 'service_type', 'stop'])

  #df1 = bus_dataset

  i = len(bus_dataset['stop'])

  x = 0

  stop_dataset = []

  for x in range(i):

    stoplist = bus_dataset['stop'][x]

    #structure URL
    stopurl = ('https://data.etabus.gov.hk/v1/transport/kmb/stop/'+ stoplist)
    #print(stopurl)

    stopresponse = requests.get(stopurl)  # Make a GET request to the URL

    # Print data returned (parsing as JSON)
    stop_payload = stopresponse.json()  # Parse `response.text` into JSON

    dataset = { 'stop' : stop_payload["data"]["stop"], 'en' : stop_payload["data"]["name_en"], 'tc' : stop_payload["data"]["name_tc"], 'stop_lat': stop_payload["data"]["lat"], 'stop_long' :stop_payload["data"]["long"]}
    stop_dataset.append(dataset)

  # #dataset
  bus_df = pd.DataFrame(data=bus_dataset, columns=['bound', 'route', 'seq', 'service_type', 'stop'])

  # #dataset1
  stop_df = pd.DataFrame(data=stop_dataset, columns=['stop', 'en', 'tc', 'stop_lat', 'stop_long'])
  result_BusCheckOutbound=[]
  result_BusCheckOutbound = pd.merge(bus_df, stop_df, how='left' , on=["stop"])

  return result_BusCheckOutbound