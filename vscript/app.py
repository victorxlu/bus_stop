from flask import Flask, jsonify, request, render_template
from getEtaBystop import getEtaBystop  # Ensure this import points to your function correctly
import os

app = Flask(__name__, template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Set template folder to the parent directory

@app.route('/')
def index():
    return render_template('index.html')  # Serve index.html from the parent directory


@app.route('/get_eta', methods=['GET'])
def get_eta():
    stop_id = request.args.get('stop_id')  # Get stop_id from query parameters

    if not stop_id:
        return jsonify({"error": "No stop ID provided."}), 400

    try:
        # Call the getEtaBystop function with the provided stop ID
        arrivals_data = getEtaBystop(stop_id)

        # Return the arrivals data wrapped in the expected structure
        return jsonify({"arrivals": {"arrivals": arrivals_data}}), 200

    except Exception as e:
        # Handle unexpected errors gracefully
        return jsonify({"error": "An unexpected error occurred.", "message": str(e)}), 500
    
    
if __name__ == '__main__':
    app.run(debug=True)