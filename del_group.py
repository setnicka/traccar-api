#!/usr/bin/python3
import csv
import requests
import sys

from conf import server, auth

def die(msg):
    print(msg, file=sys.stderr)
    exit(1)

if len(sys.argv) <= 1:
    die(f"Usage: {sys.argv[0]} <group_name>")

group_name = sys.argv[1]

# Get existing groups:
session = requests.Session()
session.auth = auth

####################

resp = session.get(f"{server}/api/groups")
if resp.status_code != 200:
    die(f"Cannot get existing groups: {resp.status_code}\n{resp.text}")

group_id: int | None = None
for group in resp.json():
    if group["name"] == group_name:
        group_id = group["id"]
        break

if group_id is None:
    die(f"No such group '{group_name}'")

####################

resp = session.get(f"{server}/api/devices")
if resp.status_code != 200:
    die(f"Cannot get existing devices: {resp.status_code}\n{resp.text}")

for device in resp.json():
    if device["groupId"] == group_id:
        print(f"Deleting device '{device['name']}' ({device['id']})")
        r = session.delete(f"{server}/api/devices/{device['id']}")
        if r.status_code != 204:
            die(f"Deleting device failed: {r.status_code}\n{r.text}")

# Delete group itself
print(f"Deleting group '{group_name}' ({group_id})")
r = session.delete(f"{server}/api/groups/{group_id}")
if r.status_code != 204:
    die(f"Deleting group failed: {r.status_code}\n{r.text}")
