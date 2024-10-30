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

@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML form

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the 'input' from the form
        input_data = request.form.get('input')  # Fetching input directly from form data

        # Check if input is provided
        if not input_data:
            return jsonify({"error": "No input provided"}), 400

        # Prepare request data for Azure AI prompt flow
        data = {'input': input_data}  # Modify according to your expected input structure
        body = json.dumps(data).encode('utf-8')  # Properly encode JSON data

        # Define your Azure endpoint and API key
        url = 'https://cxqa-genai-project-igysf.eastus.inference.ml.azure.com/score'  # Your Azure endpoint
        api_key = 'GOukNWuYMiwzcHHos35MUIyHrrknWibM'  # Your Azure API key

        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': api_key  # Use the correct header for Azure API key
        }

        # Send the request to Azure
        req = urllib.request.Request(url, body, headers)
        
        response = urllib.request.urlopen(req)  # Attempt to make the request
        result = response.read()
        
        # Parse and return the result
        return jsonify(json.loads(result)), 200  # Return the API response to the client

    except urllib.error.HTTPError as error:
        # Capture detailed error response from Azure
        error_message = error.read().decode("utf-8")  # Read the response body of the error
        print(f"HTTPError: {error.code} - {error_message}")  # Log to stdout for Azure logs
        return jsonify({
            "error": "The request failed",
            "status_code": error.code,
            "info": error_message
        }), error.code
    
    except Exception as e:
        # Log unexpected errors
        print(f"An error occurred: {str(e)}")  # Log for debugging
        return jsonify({
            "error": "An internal server error occurred",
            "details": str(e)  # Provide detailed error message for debugging
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Listen for requests
