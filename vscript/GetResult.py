
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

def GetResult(input):

    url = input
    response = requests.get(url)  # Make a GET request to the URL

    # Print data returned (parsing as JSON)

    payload = response.json()  # Parse `response.text` into JSON

    return payload