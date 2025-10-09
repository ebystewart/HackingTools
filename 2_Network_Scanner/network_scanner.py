#!/usr/bin/env python

import scapy.all as scapy
import optparse

#import argparse # incase of the replacement of optparse is to be used
# parser = argparse.ArgumentParser()
# parser.add_argument(....)
# options = parse.parse_args()
# Tips:
# use route -n command in linux to find the gateway IP
# use arp -a command in windows to find the arp table

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="IP or IP range for which ARP has to be resolved")
    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify an ip or ip range; use --help for more info")
    return options

def scan(ip):
    #scapy.arping(ip)
    arp_request = scapy.ARP(pdst=ip)
    #arp_request.pdst = ip
    # it will work without the dst="...", but will warn for every data sent out that dst is not configured and defaulting to broadcast Id
    #broadcast = scapy.Ether() 
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose = False)[0]

    clients_list = []

    for element in answered_list:
        client_dict = {"ip":element[1].psrc, "mac":element[1].hwsrc}
        #print(element[1].psrc + "\t\t" + element[1].hwsrc)
        clients_list.append(client_dict)
    return clients_list


def print_result(results_list):
    print("IP\t\t\tMAC Address\n-------------------------------------------------")
    for client in results_list:
        #print(client)
        print(client["ip"] + "\t\t" + client["mac"])
    print("-------------------------------------------------")
    

    #print(arp_request.summary())
    #scapy.ls(scapy.ARP()) # This is used to list the supported parameters of ARP()
    #arp_request.show()

    #print(broadcast.summary())
    #scapy.ls(scapy.Ether())
    #broadcast.show()

    #print(arp_request_broadcast.summary())
    #arp_request_broadcast.show()

    #print(answered_list.summary())
    #print(unanswered_list.summary())


#scan("10.0.2.2")

options = get_arguments()

#scan_result = scan("10.0.2.2/24")
scan_result = scan(options.target)
print_result(scan_result)