import socket
import os
import sys

def send_file(filename, host="127.0.0.1", port=5000):
    filesize = os.path.getsize(filename)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        # Send header first
        header = f"{os.path.basename(filename)}|{filesize}\n"
        client_socket.sendall(header.encode("utf-8"))

        # Send file contents
        with open(filename, "rb") as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                client_socket.sendall(chunk)

    print(f"File '{filename}' sent successfully.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 client.py <nr>")
        sys.exit(1)

    filename = f"log{sys.argv[1]}.txt"
    send_file(filename)

if __name__ == "__main__":
    main()