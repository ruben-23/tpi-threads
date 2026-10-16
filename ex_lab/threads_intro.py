"""Primele fire de execuție: trei senzori care măsoară în același timp."""
import threading
import time


def sensor(name, period, count):
    for i in range(1, count + 1):
        time.sleep(period)  # firul așteaptă și cedează procesorul
        print(f"{time.perf_counter() - START:4.1f} s  {name}: citirea {i}")


START = time.perf_counter()
threads = [
    threading.Thread(target=sensor, args=("temperatura", 0.5, 4)),
    threading.Thread(target=sensor, args=("umiditate", 0.7, 3)),
    threading.Thread(target=sensor, args=("co2", 1.0, 2)),
]
for t in threads:
    t.start()  # firul pornește și rulează în paralel cu restul
for t in threads:
    t.join()  # firul principal așteaptă terminarea lui t
print(f"Gata în {time.perf_counter() - START:.1f} s; secvențial ar dura 6.1 s")
