"""Formatul mesajelor schimbate între senzor și gateway."""
import json

# coloana din CSV -> cheia din mesajul JSON
FIELDS = {"Temperature": "temperature", "Humidity": "humidity",
          "Light": "light", "CO2": "co2"}
REQUIRED = ("device_id", "seq", "ts", "temperature", "co2")
CO2_LIMIT = 1000  # ppm


def build_message(row, device_id, seq):
    """Transformă un rând din CSV într-un text JSON."""
    msg = {"device_id": device_id, "seq": seq, "ts": row["date"]}
    for column, key in FIELDS.items():
        msg[key] = float(row[column])
    return json.dumps(msg)


def parse_message(text):
    """Întoarce mesajul ca dicționar sau ridică ValueError."""
    msg = json.loads(text)  # JSONDecodeError este tot un ValueError
    missing = [key for key in REQUIRED if key not in msg]
    if missing:
        raise ValueError(f"lipsesc câmpurile {missing}")
    return msg


def format_message(msg):
    """Componentele de interes, ca un singur rând de text."""
    line = (f"[{msg['seq']:>3}] {msg['device_id']}  {msg['ts']}  "
            f"T={msg['temperature']:.1f}°C  CO2={msg['co2']:.0f} ppm")
    if msg["co2"] > CO2_LIMIT:
        line += "  ALERTĂ: CO2 ridicat"
    return line


def show(msg):
    """Afișează la consolă componentele de interes."""
    print(format_message(msg))
