import requests

target_url = "google.com"

def request(url):
    try:
        get_response = requests.get("http://" + url)
        return get_response
    except requests.exceptions.ConnectionError:
        pass

with open("subdomains_sample.list", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip() # strips empty spaces in a line
        #print(line)
        test_url = word + "." + target_url
        #print(test_url)
        response = request(test_url)
        if response:
            print("[+] Discovered sub-domain ---> " + test_url)
