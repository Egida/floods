import threading
import socket
import time

class config:
    server_host: str = "0.0.0.0"
    server_port: int = 8080

class vars:
    total_rps: int = 0
    total_bps: int = 0
    rps: int = 0
    bps: int = 0

def handle(client: socket.socket) -> None:
    try:
        vars.rps += 1
        vars.total_rps += 1
        request = client.recv(4096)
        vars.bps += len(request)
        vars.total_bps += len(request)
        response_content = "<!DOCTYPE html><html><head><title>HTTP DSTAT</title></head><body><center><h1>HTTP DSTAT</h1></center></body></html>"
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {len(response_content)}\r\n\r\n{response_content}"
        client.send(response.encode())
    except Exception:
        pass

def listener(sock: socket.socket) -> None:
    while True:
        client, address = sock.accept()
        threading.Thread(target=handle, args=[client], daemon=True).start()

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
        print(f"[PROGRAM] -> STARTED")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[SOCKET] -> BINDING: {config.server_host}:{config.server_port}")
        sock.bind((config.server_host, config.server_port))
        sock.listen()
        print(f"[SOCKET] -> LISTENING: {config.server_host}:{config.server_port}")
        threading.Thread(target=listener, args=[sock], daemon=True).start()
        print(f"[NOTE] -> THE LOGS WILL PRINT OUT WHEN THE STATUS CHANGES")
        previous_data = 0
        while True:
            if vars.total_bps == previous_data:
                time.sleep(.1)
                continue
            previous_data = vars.total_bps
            print(f"[LOG] REQUESTS +=> {vars.rps} => {vars.total_rps} | BANDWIDTH +=> {bytecount(vars.bps)} => {bytecount(vars.total_bps)}")
            vars.rps = 0
            vars.bps = 0
            time.sleep(1)
    except Exception as e:
        print(f"[PROGRAM] -> ERROR: {e}")
        pass
    except KeyboardInterrupt:
        exit()
    finally:
        print(f"[PROGRAM] -> STOPPED")
        print(f"\r\n\r\n[STATISTICS]\r\nTOTAL_REQUESTS -> {vars.total_rps}\r\nTOTAL_BANDWIDTH -> {vars.total_bps}\r\n")
        try:
            sock.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
