import requests

target_url = "google.com"

def request(url):
    try:
        get_response = requests.get("http://" + url, timeout=5)
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

        with open("files-and-dirs_sample.txt", "r") as dir_file:
            for dir in dir_file:
                path = dir.strip()
                print(path)
                path_url = test_url + "/" + path
                print(path_url)
                new_response = request(path_url)
                if new_response:
                    print("\t[+] Discovered path ---> " + path)