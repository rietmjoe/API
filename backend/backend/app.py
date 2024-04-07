from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# Base URL for the OpenData API of Switzerland Tourism
BASE_URL = "https://opendata.myswitzerland.io/v1"
API_KEY = "Key" 

def get_api_data(endpoint, object_id=None):
    headers = {
        'x-api-key': 'Key',  
        # heisst evtl auch anders... Hier hatte ich Mühe
    }
    url = f"{BASE_URL}/{endpoint}"
    if object_id:
        url += f"/{object_id}"
    response = requests.get(url, headers=headers)
    return response.json()

@app.route('/api/destinations', methods=['GET'])
def get_destinations():
    return jsonify(get_api_data('destinations'))

@app.route('/api/destinations/<id>', methods=['GET'])
def get_destination_by_id(id):
    return jsonify(get_api_data('destinations', id))

@app.route('/api/attractions', methods=['GET'])
def get_attractions():
    return jsonify(get_api_data('attractions'))

@app.route('/api/attractions/<id>', methods=['GET'])
def get_attraction_by_id(id):
    return jsonify(get_api_data('attractions', id))

@app.route('/api/offers', methods=['GET'])
def get_offers():
    return jsonify(get_api_data('offers'))

@app.route('/api/offers/<id>', methods=['GET'])
def get_offer_by_id(id):
    return jsonify(get_api_data('offers', id))

@app.route('/api/tours', methods=['GET'])
def get_tours():
    return jsonify(get_api_data('tours'))

@app.route('/api/tours/<id>', methods=['GET'])
def get_tour_by_id(id):
    return jsonify(get_api_data('tours', id))

@app.route('/api/tours/<id>/geodata', methods=['GET'])
def get_tour_geodata_by_id(id):
    return jsonify(get_api_data('tours', f"{id}/geodata"))

@app.route("/")
def hello_world():
    return "<p>Welcome to the Switzerland Tourism API Service!</p>"

if __name__ == "__main__":
    print("Starting the Flask server for Switzerland Tourism API Service...")
    app.run(debug=True)
