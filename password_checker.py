import requests
import hashlib

def get_password_hash(password):
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    return sha1_hash

def check_password_pwned(password):
    sha1_hash = get_password_hash(password)
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("Error connecting to the API")

    pwned_hashes = [line.split(":")[0] for line in response.text.splitlines()]
    for pwned_suffix in pwned_hashes:
        if pwned_suffix == suffix:
            return True
    return False

if __name__ == "__main__":
    password = input("Enter a password to check: ")
    if check_password_pwned(password):
        print("This password has been compromised in a data breach. Please choose a different password.")
    else:
        print("This password has not been found in any data breaches. It is relatively safe to use.")
