import socket
import os
import sys

def send_file(filename, host='127.0.0.1', port=5000):
    #filesize = os.path.getsize(filename)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Trimitem antetul cu numele și dimensiunea fișierului
    #header = f"{filename}|{filesize}\n".encode()
    #print(header)
    #client_socket.send(header)

    # Trimitem fișierul
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(4096)
            if not bytes_read:
                # Am ajuns la sfarsitul fisierului
                break
            client_socket.sendall(bytes_read)
    print(f"Fișierul '{filename}' a fost trimis către server.")
    client_socket.close()

def main():
    if len(sys.argv) != 2:
        print("Utilizare: python3 client.py <nr>")
        sys.exit(1)

    nr = sys.argv[1]
    
    filename = f"log{nr}.txt"  
    send_file(filename)

if __name__ == '__main__':
    main()

