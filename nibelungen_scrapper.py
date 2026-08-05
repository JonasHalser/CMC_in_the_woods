import csv
from datetime import datetime
from pathlib import Path

import requests

# CMC Ticket Dashboard - Into the Woods
# Schreibt bei jedem Lauf eine neue Zeile in data/ticket_history.csv.

APPOINTMENTS = [
    ("12.02", "https://okticket.de/index.php?event_id=58398&pmp_id=44831"),
    ("13.02", "https://okticket.de/index.php?event_id=58399&pmp_id=44832"),
    ("14.02", "https://okticket.de/index.php?event_id=58400&pmp_id=44833"),
    ("19.02", "https://okticket.de/index.php?event_id=58401&pmp_id=44834"),
    ("20.02", "https://okticket.de/index.php?event_id=58402&pmp_id=44835"),
    ("21.02", "https://okticket.de/index.php?event_id=58403&pmp_id=44836"),
    ("28.03", "https://okticket.de/index.php?event_id=58404&pmp_id=44837"),
    ("29.03", "https://okticket.de/index.php?event_id=58405&pmp_id=44838"),
    ("02.04", "https://okticket.de/index.php?event_id=58406&pmp_id=44839"),
    ("03.04", "https://okticket.de/index.php?event_id=58407&pmp_id=44840"),
]

CSV_FILE = Path("data/ticket_history.csv")


def count_occupied(url: str) -> int:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        html = response.text.lower()

        occupied = html.count("occupied")
        sperr = html.count("sperr")

        return max(0, occupied + sperr - 1)

    except requests.RequestException as error:
        print(f"Fehler beim Abrufen von {url}: {error}")
        return -1


def get_last_counts() -> list[int | str]:
    """
    Liest die letzte gültige CSV-Zeile ein.

    Falls die Datei noch nicht existiert oder leer ist,
    werden leere Werte zurückgegeben.
    """
    empty_values = [""] * len(APPOINTMENTS)

    if not CSV_FILE.exists():
        return empty_values

    try:
        with CSV_FILE.open("r", newline="", encoding="utf-8") as file:
            rows = list(csv.reader(file))

        # Erwartet mindestens Kopfzeile und eine Datenzeile.
        if len(rows) < 2:
            return empty_values

        last_row = rows[-1]
        last_values = last_row[1:]

        result: list[int | str] = []

        for index in range(len(APPOINTMENTS)):
            if index >= len(last_values):
                result.append("")
                continue

            value = last_values[index].strip()

            try:
                result.append(int(value))
            except ValueError:
                result.append("")

        return result

    except (OSError, csv.Error) as error:
        print(f"Fehler beim Lesen der CSV-Datei: {error}")
        return empty_values


def write_csv() -> None:
    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    last_counts = get_last_counts()

    measured_counts = [
        count_occupied(url)
        for _, url in APPOINTMENTS
    ]

    counts: list[int | str] = []

    for measured, previous in zip(measured_counts, last_counts):
        # Bei 0 oder einem Abruffehler (-1) den letzten Wert übernehmen.
        # Ist kein vorheriger Wert vorhanden, bleibt das Feld leer.
        if measured <= 0:
            counts.append(previous)
        else:
            counts.append(measured)

    file_exists = CSV_FILE.exists()

    with CSV_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(
                ["timestamp"] + [label for label, _ in APPOINTMENTS]
            )

        writer.writerow([timestamp] + counts)

    print(f"Messwerte:  {measured_counts}")
    print(f"Gespeichert: {timestamp} -> {counts}")


if __name__ == "__main__":
    write_csv()
