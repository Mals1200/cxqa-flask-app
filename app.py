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
    # Get the 'input' from the JSON request
    input_data = request.form.get('input')  # Retrieve input from the form
    
    # Check if input is provided
    if input_data is None or input_data == "":
        return jsonify({"error": "No input provided"}), 400

    # Prepare request data for Azure AI prompt flow
    data = {'input': input_data}
    body = json.dumps(data).encode('utf-8')  # Properly encode JSON data

    url = 'https://cxqa-genai-project-igysf.eastus.inference.ml.azure.com/score'  # Your Azure endpoint
    api_key = 'GOukNWuYMiwzcHHos35MUIyHrrknWibM'  # Use your actual API key

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': api_key  # Use API key for Azure API authentication
    }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)  # Attempt to make the request to Azure
        result = response.read()  # Read the response
        
        # Parse and return the result
        return jsonify(json.loads(result)), 200  # Serve the API response to the client

    except urllib.error.HTTPError as error:
        # Log HTTP errors
        log_error_details(error)  # Call the logging function
        return jsonify({
            "error": "The request failed",
            "status_code": error.code,
            "info": error.read().decode("utf-8")
        }), error.code
    except Exception as e:
        # Handle and log all other exceptions
        log_error_details(e)
        return jsonify({
            "error": "An error occurred during the request",
            "details": str(e)  # Detailed error message for debugging
        }), 500


def log_error_details(error):
    """Function to log error details to console for diagnostics."""
    print(f"Error occurred: {str(error)}")
    if hasattr(error, 'read'):
        print(f"Error details: {error.read().decode('utf-8')}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Listen for requests
