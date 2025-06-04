from datetime import datetime
import pandas as pd
from pytz import timezone
from GetResult import GetResult  # Ensure this is the correct import

def getEtaBystop(stopid):
    try:
        input = stopid
        address = 'https://data.etabus.gov.hk/v1/transport/kmb/stop-eta/' + input
        print(f"Fetching data from: {address}")  # Debug output

        payload = GetResult(address)  # Fetch the inbound data
        print(f"Received payload: {payload}")  # Debug output

        if 'data' not in payload or not payload['data']:
            print(f"No data found for stop ID: {stopid}")  # Log the stop ID
            return []  # Return an empty list if no data is found

        # Get current time in Hong Kong timezone
        utc_now = datetime.now(timezone('UTC'))
        ts_now = utc_now.astimezone(timezone("Asia/Hong_Kong"))

        # Create DataFrame from the payload
        sp_stop_bus_dataset = pd.DataFrame(payload['data'], columns=['co', 'route', 'eta', 'dest_en', 'dest_tc', 'seq', 'service_type'])

        # Ensure 'eta' is in datetime format
        sp_stop_bus_dataset["eta"] = pd.to_datetime(sp_stop_bus_dataset["eta"])

        # Add current time to the DataFrame
        sp_stop_bus_dataset["currenttime"] = ts_now

        # Calculate the difference between ETA and current time
        sp_stop_bus_dataset['diff'] = sp_stop_bus_dataset["eta"] - sp_stop_bus_dataset["currenttime"]

        # Filter for future ETAs
        sp_stop_bus_dataset = sp_stop_bus_dataset[(~sp_stop_bus_dataset['diff'].isna()) & (sp_stop_bus_dataset['diff'] > pd.Timedelta(0))]

        # Calculate minutes until arrival
        sp_stop_bus_dataset['Minutes Arrive'] = sp_stop_bus_dataset['diff'].dt.total_seconds() / 60

        # Convert DataFrame to a list of dictionaries for easier consumption
        result = sp_stop_bus_dataset.to_dict(orient='records')

        # Include the 'diff' in a serializable way if needed
        for record in result:
            record['diff'] = record['diff'].total_seconds() if isinstance(record['diff'], pd.Timedelta) else None

        return result

    except Exception as e:
        print(f"Error in getEtaBystop: {e}")
        return []  # Return an empty list or handle the error as needed