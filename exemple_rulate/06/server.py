import socket
import threading
import time

# Configurații server
HOST = '127.0.0.1'  # Adresa IP locală
PORT = 65433        # Portul pe care ascultă serverul

# Funcția care scrie datele într-un fișier
def scrie_in_fisier(data):
    with open('date_udp.txt', 'a') as f:
        f.write(data + "\n")

def udp_server():
    # Cream socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Setăm dimensiunea buffer-ului de recepție la 8 KB
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
        s.bind((HOST, PORT))
        print(f"Serverul ascultă pe {HOST}:{PORT}")

        while True:
            # Primim date de la client
            data, addr = s.recvfrom(1024)  # Bufar de 1024 bytes
            mesaj = data.decode('utf-8')
            print(f"Primit {mesaj} de la {addr}")

            # Introducem o întârziere pentru a simula serverul care nu poate scrie rapid
            time.sleep(1)

            # Scriem datele în fișier
            scrie_in_fisier(mesaj)

if __name__ == "__main__":
    udp_server()

