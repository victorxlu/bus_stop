from datetime import datetime
import pandas as pd
from pytz import timezone
from GetResult import GetResult  # Ensure this import is correct
from webConvert import build_url

#def getEtaBystop(stopid, is_web=True):

def getEtaBystop(stopid, is_web=True):

    input = stopid

    # Construct the API address using webConvert
#    address = webConvert(f'/v1/transport/kmb/stop-eta/{input}', is_web)  # Use webConvert for URL construction
#   'https://checksushiro.alvis-lam2019.workers.dev/?url=${Uri.encodeComponent(uri.toString())}';
 
 
    input = 'https%3A%2F%2Fdata.etabus.gov.hk%2Fv1%2Ftransport%2Fkmb%2Fstop-eta%2FFE30EA565CC9ADBE'

    # Construct the API address
    address = f'https://data.etabus.gov.hk/v1/transport/kmb/stop-eta/'+input
    

#   address = build_url(address)
#   address = build_url(address)
    print(address)
    # Fetch the inbound data
    payload = GetResult(address)  # Assuming GetResult fetches the data as a dictionary

    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    
    # Get current UTC time
    utc_now = datetime.now(timezone('UTC'))
    # Convert to Hong Kong timezone
    ts_now = utc_now.astimezone(timezone("Asia/Hong_Kong"))
    print(f"Current time in Hong Kong: {ts_now.strftime(fmt)}")  # Debug output

    # Check if payload is valid and contains 'data'
    if payload is None or 'data' not in payload:
        print(f"No valid data found for stop ID: {stopid}")
        return []  # Return an empty list if no data is found

    # Check if the 'data' field is empty
    if not payload['data']:
        print(f"No data available for stop ID: {stopid}")
        return []  # Return an empty list

    # Create a DataFrame from the payload data
    sp_stop_bus_dataset = pd.DataFrame(payload['data'], columns=['route', 'eta', 'dest_en', 'dest_tc', 'seq', 'service_type'])

    # Ensure 'eta' is in datetime format
    sp_stop_bus_dataset["eta"] = pd.to_datetime(sp_stop_bus_dataset["eta"], errors='coerce')
    sp_stop_bus_dataset["currenttime"] = ts_now

    # Calculate the difference between ETA and current time
    sp_stop_bus_dataset['diff'] = sp_stop_bus_dataset["eta"] - sp_stop_bus_dataset["currenttime"]

    # Filter for future ETAs
    sp_stop_bus_dataset = sp_stop_bus_dataset[(~sp_stop_bus_dataset['diff'].isna()) & (sp_stop_bus_dataset['diff'] > pd.Timedelta(0))]

    # If no future ETAs, return an empty list
    if sp_stop_bus_dataset.empty:
        print(f"No upcoming ETAs for stop ID: {stopid}")
        return []  # Return an empty list

    # Calculate Minutes to Arrive (convert Timedelta to total seconds)
    sp_stop_bus_dataset['Minutes Arrive'] = sp_stop_bus_dataset['diff'].dt.total_seconds() / 60

    # Convert DataFrame to a list of dictionaries
    arrivals_data = sp_stop_bus_dataset.to_dict(orient='records')

    # Format dates as strings for JSON serialization
    for arrival in arrivals_data:
        arrival['eta'] = arrival['eta'].strftime(fmt)  # Format ETA as string
        arrival['currenttime'] = arrival['currenttime'].strftime(fmt)  # Format current time as string
        arrival['Minutes Arrive'] = float(arrival['Minutes Arrive'])  # Ensure it's a float

        # Ensure no Timedelta is returned; this is already done with the Minutes Arrive calculation
        # Confirming that 'diff' is not returned to the client
        if 'diff' in arrival:
            del arrival['diff']  # Ensure diff is not included

    return arrivals_data  # Return the list of dictionaries