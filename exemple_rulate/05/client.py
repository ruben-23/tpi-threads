import socket

# Configurații client
HOST = '127.0.0.1'  # Adresa IP locală a serverului (localhost)
PORT = 65432        # Portul pe care ascultă serverul

def consumator():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))  # Conectăm clientul la server
        print(f"Conectat la server {HOST}:{PORT}")

        while True:
            data = s.recv(1024)  # Primim date de la server
            if not data:
                break  # Închidem conexiunea dacă nu mai sunt date
            print(f"Consumatorul a primit: {data.decode('utf-8').strip()}")

if __name__ == "__main__":
    consumator()


