#!/usr/bin/env python

#command: iptables -I FORWARD -j NFQUEUE --queue-num 0

import scapy.all as scapy
import netfilterqueue

def process_packet(packet):
    print("[+] Filtered packet is queued in nfq 0\n")
    print(packet.show())

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

