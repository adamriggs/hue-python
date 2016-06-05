from scapy.all import *

def arp_display(pkt):
  if pkt[ARP].op == 1: #who-has (request)
    print "ARP Probe from: " + pkt[ARP].hwsrc
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      print "0.0.0.0: ARP Probe from: " + pkt[ARP].hwsrc

print "start"
print sniff(prn=arp_display, filter="arp", store=0, count=10)
print "stop"
