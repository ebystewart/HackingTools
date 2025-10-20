#!/usr/bin/env python

import scapy.all as scapy


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

def sniff(interface):
    # scapy.sniff() is a blocking call, will not return unless exception
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet) # prn is the callback function


def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            if real_mac != response_mac:
                print("[+] You are being ARP poisoned...!!!")

        except IndexError:
            pass

        except KeyboardInterrupt:
            print("[+] Detected CTRL + C.....Closing App....Please wait...")
            exit()


sniff("enp0s3")


#ref: pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org NetFilterQueue
#ref: https://gitlab.com/kalilinux/packages/python-netfilterqueue/tree/kali/master