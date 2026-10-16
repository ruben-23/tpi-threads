from datetime import datetime

line = '2023-10-01 08:15:30 Procesul B a pornit'

# Extragem primele 19 caractere (timestamp-ul)
timestamp_str = line[:19]

# Convertim șirul de caractere într-un obiect datetime
dt = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

# Calculăm timestamp-ul (numărul de secunde de la epoca Unix)
timestamp = dt.timestamp()

print("Timestamp:", timestamp)

