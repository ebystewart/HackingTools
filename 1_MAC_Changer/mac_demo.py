#!/usr/bin/env python

import subprocess

#interface = "eth0"
#new_mac = "11:22:33:44:55:66"
#subprocess.call("ifconfig " + interface + " down", shell=True)
#subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
#subprocess.call("ifconfig " + interface + " up", shell=True)

interface = input("interface > ") # use raw_input() for python2
new_mac = input("New MAC > ")

print("[+] Changing MAC address for " + interface + " to " + new_mac)

subprocess.call(["ifconfig", interface, "down"])
subprocess.call(["ifconfig", interface, "hw ether", new_mac])
subprocess.call(["ifconfig", interface, "up"])

