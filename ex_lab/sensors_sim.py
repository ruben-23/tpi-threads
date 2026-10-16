"""Simulează mai mulți senzori într-un singur proces, câte un fir pentru fiecare."""
import csv
import socket
import sys
import threading
import time

from message import build_message

HOST, PORT = "127.0.0.1", 5000
N_SENSORS = int(sys.argv[1]) if len(sys.argv) > 1 else 3
INTERVAL = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0


def run_sensor(device_id, rows):
    with socket.create_connection((HOST, PORT)) as sock:
        for seq, row in enumerate(rows, start=1):
            text = build_message(row, device_id, seq)
            sock.sendall((text + "\n").encode("utf-8"))
            time.sleep(INTERVAL)


with open("occupancy_sample.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))  # doar citită de fire: nu are nevoie de lock

threads = [threading.Thread(target=run_sensor, args=(f"sala-{101 + i}", rows))
           for i in range(N_SENSORS)]
start = time.perf_counter()
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"{N_SENSORS} senzori au terminat în {time.perf_counter() - start:.1f} s")
