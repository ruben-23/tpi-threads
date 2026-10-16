import socket
import threading
import datetime

def handle_client(connection, address, file_number):
    connection.settimeout(0.5)
    print(f"[{address}] Conexiune acceptată. Aștept fișierul {file_number}...")

    # Primim fișierul
    with open(f"received_{file_number}.txt", "wb") as f:
      while True:
        try:
            data = connection.recv(4096)
            if not data:
                break
            f.write(data)
        except socket.timeout:
            # Nu am mai primit date in intervalul de timeout
            print("Timeout!")
            break
    print(f"[{address}] Fișierul {file_number} primit cu succes.")
    connection.close()

def main():
    host = '0.0.0.0'  # Ascultă pe toate interfețele
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print(f"Serverul ascultă pe {host}:{port}")

    connections = []
    for i in range(2):
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, i+1))
        thread.start()
        connections.append(thread)

    # Așteptăm ca ambele conexiuni să se încheie
    for thread in connections:
        thread.join()

    # După ce am primit ambele fișiere, le combinăm
    merge_files("received_1.txt", "received_2.txt", "merged_log.txt")
    print("Fișierele au fost combinate și salvate în 'merged_log.txt'.")


def parse_timestamp(line):
    # Presupunem că timestamp-ul este la începutul liniei și are lungimea de 19 caractere
    timestamp_str = line[:19]
    timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    return timestamp

def read_log_file(filename):
    entries = []
    with open(filename, 'r') as f:
        for line in f:
            timestamp = parse_timestamp(line)
            entries.append((timestamp, line))
    return entries    


def merge_files(file1, file2, output_file):
    log1 = read_log_file(file1)
    log2 = read_log_file(file2)

    combined_logs = log1 + log2
    combined_logs.sort(key=lambda x: x[0]) # sorteaza dupa timestamp
    with open(output_file, 'w') as outfile:
        for entry in combined_logs:
            outfile.write(entry[1])

if __name__ == '__main__':
    main()

