import hashlib
import requests
import logging as lg

def pwned(password):

    lg.basicConfig(filename='pwned.log', level=lg.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]  
    suffix = sha1_hash[5:]  


    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if response.status_code != 200:
        lg.error(f"Error : {response.status_code}")
        raise RuntimeError(f"Error: {response.status_code}")
    found = False

    hashes = (line.split(':') for line in response.text.splitlines())
    for returned_suffix, count in hashes:
        if returned_suffix == suffix:
            found = True
            lg.info("Result is true")

    if not found :
        found = False
        lg.info("Result is false")

    return found

def pwned_description(password):

    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]  
    suffix = sha1_hash[5:]  


    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if response.status_code != 200:
        raise RuntimeError(f"Error: {response.status_code}")
    found = False

    hashes = (line.split(':') for line in response.text.splitlines())
    for returned_suffix, count in hashes:
        if returned_suffix == suffix:
            print(f"\nPassword found! Compromised {count} times.")
            found = True

    return found
