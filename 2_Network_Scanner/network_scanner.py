#!/usr/bin/env python

import scapy.all as scapy

def scan(ip):
    #scapy.arping(ip)
    arp_request = scapy.ARP(pdst=ip)
    #arp_request.pdst = ip
    broadcast = scapy.Ether()
    #broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # this step is not required as dst is of type broadcast by default

    arp_request_broadcast = broadcast/arp_request
    (answered, unanswered) = scapy.srp(arp_request_broadcast, timeout=1)

    #print(arp_request.summary())
    #scapy.ls(scapy.ARP()) # This is used to list the supported parameters of ARP()
    #arp_request.show()

    #print(broadcast.summary())
    #scapy.ls(scapy.Ether())
    #broadcast.show()

    #print(arp_request_broadcast.summary())
    #arp_request_broadcast.show()
    
    #print(answered.summary())
    #print(unanswered.summary())


# use route -n command in linux to find the gateway IP
#scan("10.0.2.2")
#scan("10.0.2.2/24")