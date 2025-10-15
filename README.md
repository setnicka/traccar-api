# Traccar API scripts

Collection of scripts for quick import, list and manage multiple devices using
Traccar API.

## API access

Set server and auth in the `conf.py`:

```py
server = "https://traccar.your.domain"  # without trailing /
auth = ("login@your.domain", "password")
```

## Adding/listing groups

Add group using Traccar web UI.

To list all available groups for your account run `list_groups.py`:

```sh
$ ./list_groups.py | jq
[
  {
    "id": 42,
    "attributes": {},
    "groupId": 0,
    "name": "MyGroup"
  }
]
```

## Adding devices

Add devices from `data.csv` to given group.

Prepare `data.csv` looking like bellow:
* `id` is an identificator used by the device
* `name` is displayed name in the Traccar
* `group` is the `id` parameter from the previous step
* `category` could be  optional

```csv
id,name,group,category
idAA,AA,42,person
idBB,BB,42,person
```

Then run:

```sh
$ ./add_devices data.csv | jq
[
  {
    "id": 216,
    "groupId": 42,
    "name": "AA",
    "uniqueId": "idAA",
    "category": "person",
    …
  },
  {
    "id": 217,
    "groupId": 42,
    "name": "BB",
    "uniqueId": "idBB",
    "category": "person",
    …
  }
]
```

## List devices

Show all devices from all available groups for your account:

```sh
$ ./list_devices.py | jq
[
  {
    "id": 216,
    "groupId": 42,
    "name": "AA",
    "uniqueId": "idAA",
    "category": "person",
    …
  },
  {
    "id": 217,
    "groupId": 42,
    "name": "BB",
    "uniqueId": "idBB",
    "category": "person",
    …
  }
]
```

## Mass delete group and devices

Delete whole group and all devices in it:

```sh
$ ./del_group.py MyGroup
Deleting device 'AA' (216)
Deleting device 'BB' (217)
Deleting group 'MyGroup' (42)
```
