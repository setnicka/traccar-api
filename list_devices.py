#!/usr/bin/python3
import csv
import requests
import sys

from conf import server, auth

def die(msg):
    print(msg, file=sys.stderr)
    exit(1)

# Get existing devices:
session = requests.Session()
session.auth = auth

resp = session.get(f"{server}/api/devices")
if resp.status_code != 200:
    die(f"Cannot get existing devices: {resp.status_code}\n{resp.text}")

print(resp.text)  # use with jq
