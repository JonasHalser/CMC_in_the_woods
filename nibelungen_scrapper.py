import csv
import os
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
    """Zählt belegte Plätze anhand des okticket-HTMLs."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; CMC-Ticket-Dashboard/1.0)",
        "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        html = response.text.lower()
        return html.count("occupied")
    except Exception as exc:
        print(f"Fehler bei {url}: {exc}")
        return -1


def write_csv() -> None:
    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    counts = [count_occupied(url) for _, url in APPOINTMENTS]
    file_exists = CSV_FILE.exists()

    with CSV_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp"] + [label for label, _ in APPOINTMENTS])
        writer.writerow([timestamp] + counts)

    print(f"Geschrieben: {timestamp} -> {counts}")


if __name__ == "__main__":
    write_csv()
