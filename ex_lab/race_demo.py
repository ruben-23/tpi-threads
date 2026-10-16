"""Condiție de cursă: patru fire numără mesaje în același contor."""
import threading
import time

stats = {"total": 0}
lock = threading.Lock()
messages_count = 100000
threads_count = 80

def count_message():
    value = stats["total"]  # 1. citește
    time.sleep(0)  # aici poate rula alt fir
    stats["total"] = value + 1  # 2. scrie


def receiver(n, use_lock):
    for _ in range(n):
        if use_lock:
            with lock:  # secțiune critică: un singur fir odată
                count_message()
        else:
            count_message()


for use_lock in (False, True):
    stats["total"] = 0
    threads = [threading.Thread(target=receiver, args=(messages_count, use_lock))
               for _ in range(threads_count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"cu lock={use_lock}: {stats['total']} din {threads_count * messages_count} mesaje numărate")
