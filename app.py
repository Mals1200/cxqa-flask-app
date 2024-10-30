from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.json['input']
    return jsonify({"response": f"Received input: {input_data}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
