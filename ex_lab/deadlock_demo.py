"""Blocaj: două fire cer aceleași două lock-uri, în ordine inversă."""
import threading
import time

storage_lock = threading.Lock()  # protejează stocarea
log_lock = threading.Lock()  # protejează jurnalul


def worker(name, first, second):
    with first:
        time.sleep(0.1)  # între timp, celălalt fir ia al doilea lock
        if second.acquire(timeout=2):  # fără timeout: așteptare infinită
            second.release()
            print(name, "a terminat")
        else:
            print(name, "blocat: celălalt fir ține lock-ul de care am nevoie")


a = threading.Thread(target=worker, args=("A", storage_lock, log_lock))
b = threading.Thread(target=worker, args=("B", log_lock, storage_lock))
a.start()
b.start()
a.join()
b.join()
