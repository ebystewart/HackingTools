#!/usr/bin/env python

import subprocess
import optparse
import re

#Test: python3 mac_changer.py -i eth0 -m 11:22:33:33:22:11
#      python3 mac_changer.py -i enp0s3 -m 11:22:33:33:22:11

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface for which MAC is to be changed")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    #return parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface; use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify a MAC; use --help for more info")
    return options

def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    # execute the command using check_output() API. This is alternative to call, but calpures and resturns the result of the command
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    #print(ifconfig_result)
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        printf("[-] Could not read MAC address")

options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)

if current_mac == options.new_mac:
    printf("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address change failed")