from flask import Flask, request, render_template, jsonify
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

# Home route
@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML form

# Predict route
@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.form.get('input')  # Get input from the form submission
    
    if not input_data:
        return jsonify({"error": "No input provided"}), 400  # Return an error response if input is empty

    # Prepare request data for Azure AI prompt flow
    data = {'input': input_data}  # Structure should match your Azure Prompt Flow input
    body = str.encode(json.dumps(data))

    url = 'https://cxqa-genai-project-igysf.eastus.inference.ml.azure.com/score'  # Your Azure endpoint
    api_key = 'GOukNWuYMiwzcHHos35MUIyHrrknWibM'  # Ensure your API key is managed securely
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_key
    }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        return jsonify(json.loads(result)), 200  # Return the response to the client
    except urllib.error.HTTPError as error:
        return jsonify({
            "error": "The request failed",
            "status_code": error.code,
            "info": error.read().decode("utf8", 'ignore')
        }), error.code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Local testing
