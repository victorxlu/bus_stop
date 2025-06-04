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

def BusCheckCirBound(BusNumber):

  input = BusNumber

  address = 'https://data.etabus.gov.hk/v1/transport/kmb/route-eta/'+input+'/1'

  payload = GetResult(address)  #inbound

  #print(payload)

  #bus_dataset = pd.DataFrame(payload['data'], columns=['co', 'route', 'dir', 'service_type', 'seq', 'dest_tc', 'dest_sc', 'dest_en', 'eta_seq', 'eta', 'rmk_tc', 'rmk_sc', 'rmk_en', 'data_timestamp'])
  bus_dataset = pd.DataFrame(payload['data'], columns=['co', 'route', 'seq', 'dest_tc', 'dest_en', 'eta_seq', 'eta'])

  #bus_dataset = bus_dataset.drop_duplicates(subset=['seq'])

  #df1 = bus_dataset

  i = len(bus_dataset['seq'])

  return bus_dataset
