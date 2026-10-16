"""GIL: firele nu accelerează calculul pur în Python; procesele da."""
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def cpu_work(n):
    return sum(i * i for i in range(n))


def io_work(_):
    time.sleep(0.5)  # simulează așteptarea unui mesaj din rețea


def timed(label, pool_cls, func, args):
    start = time.perf_counter()
    with pool_cls(max_workers=4) as pool:
        list(pool.map(func, args))
    print(f"{label:<22} {time.perf_counter() - start:5.2f} s")


if __name__ == "__main__":
    work = [3_000_000] * 4
    start = time.perf_counter()
    for n in work:
        cpu_work(n)
    print(f"{'calcul, secvențial':<22} {time.perf_counter() - start:5.2f} s")
    timed("calcul, 4 fire", ThreadPoolExecutor, cpu_work, work)
    timed("calcul, 4 procese", ProcessPoolExecutor, cpu_work, work)
    timed("așteptare, 4 fire", ThreadPoolExecutor, io_work, range(4))
