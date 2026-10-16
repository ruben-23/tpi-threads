# TPI.03 – Fire de execuție și concurență

Exemple de concepte (rulați fiecare separat):
- `threads_intro.py` – trei fire care simulează trei senzori
- `race_demo.py` – condiție de cursă și corectarea ei cu Lock
- `deadlock_demo.py` – blocaj între două fire, detectat cu timeout
- `gil_demo.py` – fire față de procese, pentru calcul și pentru așteptare

Aplicația client–server:
- `gateway_threads.py` – gateway TCP concurent (un fir pe senzor, coadă, fir de procesare, statistici)
- `sensors_sim.py` – mai mulți senzori simulați într-un singur proces
- `message.py`, `occupancy_sample.csv` – preluate din TPI.02 (am adăugat `format_message`)

Rulare, în două terminale:

    python gateway_threads.py
    python sensors_sim.py 3 0.2      # 3 senzori, câte un mesaj la 0,2 s

Opriți gateway-ul cu Ctrl+C: afișează statisticile finale.
`occupancy_sample.csv` conține valori sintetice în formatul UCI Occupancy Detection.
