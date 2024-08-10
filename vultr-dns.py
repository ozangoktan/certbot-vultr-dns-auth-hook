#!/usr/bin/env python

import requests
import sys
import os
import string
from time import sleep

# Configure here
VULTR_API_KEY = "put your api key here"
VULTR_BIND_DELAY = 30


def vultr_request(method, zone, path, data=None):
    url = f"https://api.vultr.com/v2/domains{zone}{path}"

    resp = requests.request(method, url, json=data, headers={
                            "Authorization": "Bearer " + VULTR_API_KEY})
    resp.raise_for_status()
    if resp.headers["Content-Type"] == "application/json":
        return resp.json()
    return resp.text


def find_zone_for_name(domain):
    resp = vultr_request("GET", "", "")
    zones = [entry["domain"] for entry in resp["domains"]]

    # api doesn't have a trailing . on its zones
    if domain[-1:] == ".":
        domain = domain[:-1]

    domain_split = domain.split(".")
    while len(domain_split) > 0:
        search = ".".join(domain_split)
        if search in zones:
            return search
        domain_split = domain_split[1:]

    raise Exception(f"Could not identify existing zone for {domain}")


def list_records(zone):
    return vultr_request("GET", "/" + zone, "/records")


def create_record(domain, txt_value):
    to_add = f"_acme-challenge.{domain}".lower()
    print(f"Creating {to_add} TXT: {txt_value}")
    zone = find_zone_for_name(domain)
    create_params = {"name": to_add, "type": "TXT", "data": f"'{txt_value}'"}
    vultr_request("POST", "/" + zone, "/records", create_params)

    print("Will sleep {} seconds to wait for DNS cluster to reload".
          format(VULTR_BIND_DELAY))
    sleep(VULTR_BIND_DELAY)


def remove_record(domain, txt_value):
    to_remove = f"_acme-challenge.{domain}".lower()
    zone = find_zone_for_name(to_remove)
    recs = list_records(zone)

    print(f"Removing {to_remove} TXT: {txt_value}")

    to_remove = to_remove[:-len(zone)-1]

    found = [rec for rec in recs["records"] if rec.get("name") == to_remove and rec.get("type") == "TXT" and rec["data"] == f"\"\'{txt_value}\'\""]
    if len(found) == 0:
        print("Could not find record to remove: {} with value {}".
              format(to_remove, txt_value))
        return

    vultr_request("DELETE", "/" + zone, "/records/" + found[0]["id"])


act = sys.argv[1]

if act == "create":
    create_record(os.environ["CERTBOT_DOMAIN"],
                  os.environ["CERTBOT_VALIDATION"])
elif act == "delete":
    remove_record(os.environ["CERTBOT_DOMAIN"],
                  os.environ["CERTBOT_VALIDATION"])
else:
    print(f"Unknown action: {act}")
    exit(1)
