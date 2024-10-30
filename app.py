from flask import Flask, request, render_template, jsonify
import urllib.request
import json
import os
import ssl

app = Flask(__name__)

def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Fetching input directly from form data
        input_data = request.form.get('input')

        if not input_data:
            return jsonify({"error": "No input provided"}), 400

        # Prepare the input for the request
        data = {
            "question": input_data,
            "chat_history": []  # You can modify this based on your application state
        }
        body = json.dumps(data).encode('utf-8')  # Properly encode JSON data

        url = 'https://cxqa-genai-project-igysf.eastus.inference.ml.azure.com/score'  # Your Azure endpoint
        api_key = 'GOukNWuYMiwzcHHos35MUIyHrrknWibM'  # Your Azure API key

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + api_key  # Use Bearer token format for authorization
        }

        req = urllib.request.Request(url, body, headers)

        # Make the request to the Azure endpoint
        with urllib.request.urlopen(req) as response:
            result = response.read()
            return jsonify(json.loads(result)), 200  # Return the API response to the client

    except urllib.error.HTTPError as error:
        error_message = error.read().decode("utf-8")  # Capture detailed error response from Azure
        print(f"HTTPError: {error.code} - {error_message}")  # Log to stdout for Azure logs
        return jsonify({
            "error": "The request failed",
            "status_code": error.code,
            "info": error_message
        }), error.code
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")  # Log for debugging
        return jsonify({
            "error": "An internal server error occurred",
            "details": str(e)  # Provide detailed error message for debugging
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the Flask app
