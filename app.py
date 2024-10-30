from flask import Flask, request, jsonify
import urllib.request
import json
import os
import ssl

app = Flask(__name__)

def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)  # Needed if using self-signed certificates.

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.json['input']

    # Prepare request data for Azure AI prompt flow
    data = {'input': input_data}
    body = json.dumps(data).encode('utf-8')
    
    url = 'https://cxqa-genai-project-igysf.eastus.inference.ml.azure.com/score'  # Your prompt flow URL
    api_key = 'GOukNWuYMiwzcHHos35MUIyHrrknWibM'  # Your API key, securely manage this in production

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_key
    }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        return jsonify(json.loads(result)), 200  # Parse response JSON and return
    except urllib.error.HTTPError as error:
        return jsonify({'error': str(error.code), 'message': error.read().decode("utf-8", 'ignore')}), error.code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
