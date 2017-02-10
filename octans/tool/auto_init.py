import requests
import json
import time
import socket
import datetime
import uuid
from sys import argv
myname = socket.getfqdn(socket.gethostname())
myaddr = socket.gethostbyname(myname)
requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False

import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='/root/myapp.log',
                filemode='w')

def retry(attempt):
    def decorator(func):
        def wrapper(*args, **kw):
            att = 0
            while att < attempt:
                try:
                    return func(*args, **kw)
                except Exception as e:
                    att += 1
                    print("retry curl ceres to%s"%(att))
                    time.sleep(1)
        return wrapper
    return decorator

@retry(attempt=600)
def check_task_status(task_id):
    payload = {"id":task_id,"name":""}
    headers ={'content-type': 'application/json',
            'X-CORRELATION-ID': str(uuid.uuid1()),
            'X-SOURCE': 'jupiter',
            'Authorization':'Basic bmlra2lfdGVzdDAwMkBzaW5hLmNuOjEyMzIyMw==',
            'Cache-Control':'no-cache'}
    r = requests.post("http://127.0.0.1:8000/api/check",data=json.dumps(payload), headers=headers)
    if r.json().has_key("content"):
        if  r.json()["content"].has_key("task"):
            if r.json()["content"]["task"].has_key("status"):
                if r.json()["content"]["task"]["status"] == 2:
                    return "success"
    raise Exception("Run task's Exception raised!")

@retry(attempt=10)
def run_task_over():
    import uuid
#    import pdb;pdb.set_trace()
    logging.info('This is info message %s' %(argv[1]))
    payload = {"nodes":[argv[1]],
        "tasks":["init"],
        "tasktype": "ansible_role",
        "user": "root",
        "name":myaddr+myaddr+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "fork_num": 5}
    headers ={'content-type': 'application/json',
              'X-CORRELATION-ID': str(uuid.uuid1()),
              'X-SOURCE':'jupiter',
              'Cache-Control':'no-cache'}
    r = requests.post("http://127.0.0.1:8000/api/run",data=json.dumps(payload), headers=headers)
    logging.info('This is result %s' %(r.json()))
    task_id = 123
    if r.json().has_key("content"):
        if  r.json()["content"].has_key("id"):
            print(r.json()['content']['id'])
            task_id = r.json()['content']['id']
            time.sleep(10)
            task_status = check_task_status(task_id)
            if task_status == "success":
                return
    raise Exception("Run task's Exception raised!")

run_task_over()

