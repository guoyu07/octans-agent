import requests
import json
import socket
import os
import hashlib
from sys import argv
from Crypto.PublicKey import RSA

myname = socket.getfqdn(socket.gethostname())
myaddr = socket.gethostbyname(myname)

def report_status():
    payload = {
                "InstanceId": argv[1],
                "Status": 1
                }

    headers ={'content-type': 'application/json',
              'Cache-Control':'no-cache',
              'App-Id':'tPa6NY5FDI9Fl3ie',
              'App-Key':'49sSs39RA614TLeVzLT2Z68Y4uY3BwZ7'}
    res = requests.post("http://127.0.0.1:7070/v1/instance/status",
                        data=json.dumps(payload),
                        headers=headers)
    if res.json().has_key("code"):
        if res.json()["code"] == 0:
            print(res.json())
            return
    raise Exception("report over")

report_status()
