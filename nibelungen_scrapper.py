import csv
import os
from datetime import datetime
from pathlib import Path

import requests

# CMC Ticket Dashboard - Into the Woods
# Schreibt bei jedem Lauf eine neue Zeile in data/ticket_history.csv.

APPOINTMENTS = [
    ("12.02", "https://okticket.de/tickets-musical-into-the-woods-ab-in-den-wald-straubing-theater-am-hagen-2027-02-12-e58398"),
    ("13.02", "https://okticket.de/tickets-musical-into-the-woods-ab-in-den-wald-straubing-theater-am-hagen-2027-02-13-e58399"),
    ("14.02", "https://okticket.de/tickets-musical-into-the-woods-ab-in-den-wald-straubing-theater-am-hagen-2027-02-14-e58400"),
    ("19.02", "https://okticket.de/tickets-musical-into-the-woods-ab-in-den-wald-straubing-theater-am-hagen-2027-02-19-e58401"),
    ("20.02", "https://okticket.de/tickets-musical-into-the-woods-ab-in-den-wald-straubing-theater-am-hagen-2027-02-20-e58402"),
    ("21.02", "https://okticket.de/tickets-musical-into-the-woods-ab-in-den-wald-straubing-theater-am-hagen-2027-02-21-e58403"),
    ("28.03", "https://okticket.de/tickets-musical-into-the-woods-ab-in-den-wald-straubing-theater-am-hagen-2027-03-28-e58404"),
    ("29.03", "https://okticket.de/tickets-musical-into-the-woods-ab-in-den-wald-straubing-theater-am-hagen-2027-03-29-e58405"),
    ("02.04", "https://okticket.de/tickets-musical-into-the-woods-ab-in-den-wald-straubing-theater-am-hagen-2027-04-02-e58406"),
    ("03.04", "https://okticket.de/tickets-musical-into-the-woods-ab-in-den-wald-straubing-theater-am-hagen-2027-04-03-e58407"),
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
