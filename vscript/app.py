from flask import Flask, request, jsonify, send_from_directory
import os
from getEtaBystop import getEtaBystop  # Ensure this import points to your function correctly

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')), 'index.html')

@app.route('/get_eta', methods=['GET'])
def get_eta():
    stop_id = request.args.get('stop_id')  # Get stop_id from the query parameters
    if not stop_id:
        return jsonify({'error': 'Stop ID is required'}), 400  # Return an error if stop_id is not provided

    try:
        arrivals = getEtaBystop(stop_id)  # Call the function to get ETA directly
        
        if not arrivals:
            return jsonify({'error': 'No data found for the provided Stop ID.'}), 404

        return jsonify({'arrivals': arrivals})

    except Exception as e:
        # Log the error message to the console for debugging
        print(f"Error while fetching ETA for stop ID {stop_id}: {str(e)}")  # Detailed error logging
        return jsonify({'error': 'An unexpected error occurred.', 'message': str(e)}), 500  # Return the error message

if __name__ == "__main__":
    app.run(debug=True)  # Start the Flask application