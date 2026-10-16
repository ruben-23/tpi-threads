import time
import random
from concurrent.futures import ThreadPoolExecutor

# Funcția care va fi rulată în fiecare fir
def sarcina(nr):
    print(f"Execut sarcina {nr}")
    timp_sleep = random.uniform(0.5, 2.0)  # Întârziere aleatorie între 0.5 și 2 secunde
    time.sleep(timp_sleep)
    print(f"Sarcina {nr} terminată după {timp_sleep:.2f} secunde")
    return nr

if __name__ == "__main__":
    # Cream un ThreadPoolExecutor cu 3 fire
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Programăm 5 sarcini pentru a fi executate de pool-ul de fire
        future_list = [executor.submit(sarcina, i) for i in range(5)]

        # Așteptăm terminarea tuturor sarcinilor
        for future in future_list:
            rezultat = future.result()  # Obținem rezultatul (în acest caz, doar numărul sarcinii)
            print(f"Rezultatul sarcinii {rezultat} a fost obținut")


