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

allowSelfSignedHttps(True)  # Needed if using a self-signed certificate

@app.route('/')
def home():
    return render_template('index.html')  # Serve HTML form

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input from the form submission
        input_data = request.form.get('input')

        # Check if input is provided
        if not input_data:
            return jsonify({"error": "No input provided"}), 400

        # Prepare request data for Azure AI prompt flow
        data = {'input': input_data}  # Modify input structure if needed
        body = json.dumps(data).encode('utf-8')  # Encode to JSON format

        # Azure endpoint and API key
        url = 'https://cxqa-genai-project-igysf.eastus.inference.ml.azure.com/score'
        api_key = 'GOukNWuYMiwzcHHos35MUIyHrrknWibM'  # Replace with your actual key

        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': api_key  # Correct usage for Azure API key
        }

        # Send request to Azure
        req = urllib.request.Request(url, body, headers)
        response = urllib.request.urlopen(req)  # Call to Azure
        result = response.read()
        
        # Return parsed result
        return jsonify(json.loads(result)), 200

    except urllib.error.HTTPError as error:
        # Capture detailed error response from Azure
        error_message = error.read().decode("utf-8")
        print(f"HTTPError: {error.code} - {error_message}")  # Log error details
        return jsonify({
            "error": "The request failed",
            "status_code": error.code,
            "info": error_message
        }), error.code
    
    except Exception as e:
        # Log unexpected exceptions
        print(f"An error occurred: {str(e)}")  # Log details for debugging
        return jsonify({
            "error": "An internal server error occurred",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the app
