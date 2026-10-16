import socket
import time

# Configurații client
HOST = '127.0.0.1'  # Adresa IP a serverului
PORT = 65433        # Portul serverului

def udp_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        for i in range(1000):
            mesaj = f"Mesajul {i}"
            s.sendto(mesaj.encode('utf-8'), (HOST, PORT))
            print(f"Trimis: {mesaj}")
            
            # Clientul trimite foarte rapid datele
            time.sleep(0.01)  # Interval scurt între trimiteri (50ms)

if __name__ == "__main__":
    udp_client()


