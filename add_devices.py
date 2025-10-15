#!/usr/bin/python3
import csv
import requests
import sys

from conf import server, auth

def die(msg):
    print(msg, file=sys.stderr)
    exit(1)


if len(sys.argv) <= 1:
    die(f"Usage: {sys.argv[0]} [filename.csv]")

devices_file = sys.argv[1]

# Parse devices to add
devices: dict[str, tuple[str, int, str | None]] = {}
with open(devices_file, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        devices[row["id"]] = (row["name"], int(row["group"]), row.get("category"))

# Get existing devices:
session = requests.Session()
session.auth = auth

resp = session.get(f"{server}/api/devices")
if resp.status_code != 200:
    die(f"Cannot get existing devices: {resp.status_code}\n{resp.text}")
for existing in resp.json():
    if existing["uniqueId"] in devices:
        die(f"Conflict: device with uniqueId '{existing['uniqueId']}' already exists: {existing}")

for unique_id, (name, group_id, category) in devices.items():
    data = {
        "name": name,
        "uniqueId": unique_id,
        "groupId": group_id,
    }
    if category is not None:
        data["category"] = category
    resp = session.post(f"{server}/api/devices", json=data)
    if resp.status_code != 200:
        die(f"ERROR: {resp.status_code} - {resp.text}")

response = session.get(f"{server}/api/devices")
print(response.text)
