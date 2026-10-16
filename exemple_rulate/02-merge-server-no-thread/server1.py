import socket

def receive_line(connection):
    """Read one newline-terminated header."""
    data = bytearray()

    while True:
        byte = connection.recv(1)

        if not byte:
            raise ConnectionError("Connection closed before header completed")

        if byte == b"\n":
            return data.decode("utf-8")

        data.extend(byte)

def receive_exactly(connection, filesize, output_file):
    """Receive exactly filesize bytes, or raise if the connection closes early."""
    remaining = filesize

    with open(output_file, "wb") as f:
        while remaining > 0:
            chunk = connection.recv(min(4096, remaining))

            if not chunk:
                raise ConnectionError("Connection closed before file was fully received")

            f.write(chunk)
            remaining -= len(chunk)

def handle_client(connection, address, file_number):
    print(f"[{address}] Connection accepted.")

    try:
        header = receive_line(connection)
        filename, filesize_text = header.split("|", 1)
        filesize = int(filesize_text)

        if filesize < 0:
            raise ValueError("Invalid file size")

        output_file = f"received_{file_number}.txt"

        print(f"Receiving {filename}: {filesize} bytes")

        receive_exactly(connection, filesize, output_file)

        print(f"File saved as '{output_file}'.")

    except (ValueError, ConnectionError, OSError) as e:
        print(f"[{address}] Transfer failed: {e}")

    finally:
        connection.close()

def merge_files(file1, file2, output_file):
    with open(output_file, "wb") as outfile:
        for filename in (file1, file2):
            with open(filename, "rb") as infile:
                while True:
                    chunk = infile.read(4096)
                    if not chunk:
                        break
                    outfile.write(chunk)

def main():
    host = "0.0.0.0"
    port = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(2)

        print(f"Server listening on {host}:{port}")

        for i in range(2):
            conn, addr = server_socket.accept()
            handle_client(conn, addr, i + 1)

    merge_files("received_1.txt", "received_2.txt", "merged_log.txt")
    print("Files merged into 'merged_log.txt'.")

if __name__ == "__main__":
    main()