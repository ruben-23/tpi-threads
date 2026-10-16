"""Gateway concurent: un fir pentru fiecare senzor, o coadă și un fir de procesare."""
import logging
import queue
import socket
import threading
import time

from message import format_message, parse_message

logging.basicConfig(level=logging.INFO, datefmt="%H:%M:%S",
                    format="%(asctime)s %(threadName)-10s %(message)s")
log = logging.getLogger("gateway")  # un rând de jurnal nu se amestecă cu altul

HOST, PORT = "0.0.0.0", 5000
messages = queue.Queue()  # sigură pentru mai multe fire
stats = {}  # device_id -> mesaje procesate
stats_lock = threading.Lock()


def handle_sensor(conn, addr):
    """Rulează într-un fir separat pentru fiecare senzor conectat."""
    with conn, conn.makefile("r", encoding="utf-8") as stream:
        for line in stream:
            try:
                messages.put(parse_message(line))  # producător
            except ValueError as err:
                log.warning("mesaj respins de la %s: %s", addr, err)
    log.info("senzor deconectat: %s", addr)


def process_messages():
    """Un singur fir consumă coada: afișează și numără."""
    while True:
        msg = messages.get()  # așteaptă până apare un mesaj
        log.info(format_message(msg))
        with stats_lock:
            stats[msg["device_id"]] = stats.get(msg["device_id"], 0) + 1


def report(period):
    """Afișează periodic numărul de mesaje pe senzor."""
    while True:
        time.sleep(period)
        with stats_lock:
            snapshot = dict(stats)  # copie, făcută sub lock
        log.info("statistici: %s", snapshot)


threading.Thread(target=process_messages, name="procesare", daemon=True).start()
threading.Thread(target=report, args=(5,), name="raport", daemon=True).start()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen()
    log.info("ascult pe portul %d", PORT)
    try:
        while True:
            conn, addr = srv.accept()  # firul principal doar acceptă
            log.info("senzor conectat: %s", addr)
            threading.Thread(target=handle_sensor, args=(conn, addr),
                             name=f"senzor-{addr[1]}", daemon=True).start()
    except KeyboardInterrupt:  # Ctrl+C
        with stats_lock:
            log.info("oprire; statistici finale: %s", stats)
