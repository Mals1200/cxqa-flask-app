from flask import Flask, request, jsonify
import urllib.request
import json
import os
import ssl

app = Flask(__name__)

def allowSelfSignedHttps(allowed):
    # Bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)  # Needed if you use a self-signed certificate in your scoring service.

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask app!"})

@app.route('/predict', methods=['POST'])
def predict():
    # Get the 'input' from the JSON request body
    input_data = request.json.get('input', None)
    
    # Check if the input is provided
    if input_data is None:
        return jsonify({"error": "No input provided"}), 400  # Return an error response

    # Prepare request data for Azure AI prompt flow
    data = {'input': input_data}  # Modify according to your expected input structure
    body = str.encode(json.dumps(data))

    url = 'https://cxqa-genai-project-igysf.eastus.inference.ml.azure.com/score'  # Your Azure endpoint
    api_key = 'GOukNWuYMiwzcHHos35MUIyHrrknWibM'  # Make sure to handle this safely!

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_key
    }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        
        # Parse the response from the Azure AI service
        return jsonify(json.loads(result)), 200  # Return the response to the client
    except urllib.error.HTTPError as error:
        return jsonify({
            "error": "The request failed",
            "status_code": error.code,
            "info": error.read().decode("utf8", 'ignore')
        }), error.code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Local testing
