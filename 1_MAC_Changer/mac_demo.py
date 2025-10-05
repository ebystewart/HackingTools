#!/usr/bin/env python

import subprocess
import optparse
import re

#Test: python3 mac_demo.py -i eth0 -m 11:22:33:33:22:11

#interface = "eth0"
#new_mac = "11:22:33:44:55:66"
#subprocess.call("ifconfig " + interface + " down", shell=True)
#subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
#subprocess.call("ifconfig " + interface + " up", shell=True)

#interface = input("interface > ") # use raw_input() for python2
#new_mac = input("New MAC > ")

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface for which MAC is to be changed")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    #return parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface; use --help for more info")
    elif not options.new_mac:
        parse.error("[-] Please specify a MAC; use --help for more info")
    return options

def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])



#interface = options.interface
#new_mac = options.new_mac
#(options, arguments) = get_arguments()
options = get_arguments()
change_mac(options.interface, options.new_mac)


