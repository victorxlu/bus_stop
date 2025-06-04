import pandas as pd
from datetime import datetime
from pytz import timezone
from GetResult import GetResult  # Ensure this import is correct

def getEtaBystop(stopid):
    try:
        input = stopid
        address = f'https://data.etabus.gov.hk/v1/transport/kmb/stop-eta/{input}'
        print(f"Fetching data from: {address}")  # Debug output

        payload = GetResult(address)  # Fetch the inbound data
        print(f"Received payload: {payload}")  # Debug output

        if 'data' not in payload or not payload['data']:
            print(f"No data found for stop ID: {stopid}")  # Log the stop ID
            return {'arrivals': []}  # Return an empty array if no data is found

        # Create a DataFrame from the payload data
        sp_stop_bus_dataset = pd.DataFrame(payload['data'])

        # Ensure 'eta' is in datetime format
        sp_stop_bus_dataset['eta'] = pd.to_datetime(sp_stop_bus_dataset['eta'])
        
        # Get current time in Hong Kong timezone
        utc_now = datetime.now(timezone('UTC'))
        ts_now = utc_now.astimezone(timezone("Asia/Hong_Kong"))

        # Add current time to the DataFrame
        sp_stop_bus_dataset["currenttime"] = ts_now

        # Calculate the difference between ETA and current time
        sp_stop_bus_dataset['diff'] = sp_stop_bus_dataset["eta"] - sp_stop_bus_dataset["currenttime"]

        # Filter for future ETAs
        sp_stop_bus_dataset = sp_stop_bus_dataset[(~sp_stop_bus_dataset['diff'].isna()) & (sp_stop_bus_dataset['diff'] > pd.Timedelta(0))]

        # Calculate Minutes to Arrive (convert Timedelta to total seconds)
        sp_stop_bus_dataset['Minutes Arrive'] = sp_stop_bus_dataset['diff'].dt.total_seconds() / 60

        # Convert DataFrame to a list of dictionaries for easier consumption
        result = sp_stop_bus_dataset[['route', 'dest_en', 'dest_tc', 'Minutes Arrive']].to_dict(orient='records')

        # Return the result as a JSON response without nesting
        return {'arrivals': result}  # Ensure this is the correct format

    except Exception as e:
        print(f"Error in getEtaBystop: {e}")
        return {'error': 'An unexpected error occurred.'}  # Return a generic error message