#!/usr/bin/env python

#command 1: sudo iptables -I FORWARD -j NFQUEUE --queue-num 0
#           sudo iptables -I INPUT -j NFQUEUE --queue-num 0
#           sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0
#command 2: sudo iptables --flush
#command 3: ping -c 1 bing.com
#commend 4: bettercap -iface enp0s3 -caplet hstshijack/hstshijack


import scapy.all as scapy
import netfilterqueue


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    del packet[scapy.IP].len

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())  # convert to scapy format
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet.haslayer(scapy.TCP): 
            if scapy_packet[scapy.TCP].dport == 80:
                print("[+] Request")
                print(scapy_packet.show())
            elif scapy_packet[scapy.TCP].sport == 80:
                print("[+] Response")
                print(scapy_packet.show())



    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

