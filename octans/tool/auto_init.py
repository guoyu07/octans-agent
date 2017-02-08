import requests
import json
import time
import socket
import datetime
myname = socket.getfqdn(socket.gethostname())
myaddr = socket.gethostbyname(myname)

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
@retry(attempt=1000)
def run_task_over():
	import uuid
#    import pdb;pdb.set_trace()
    payload = {"node":myaddr,
        "tasks":["init"],
        "tasktype": "ansible_role",
        "user": "root",
	    "name":myaddr+myaddr+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
	    "fork_num": 5}
    headers ={'content-type': 'application/json',
	          'X-CORRELATION-ID': str(uuid.uuid1()),
	          'X-SOURCE':'jupiter'
              'Cache-Control':'no-cache'}
    r = requests.post("http://127.0.0.1:8000/task/run",data=json.dumps(payload), headers=headers)
    if r.json().has_key("status"):
        if r.json()["status"] == "started":
            print(r.json())
            return
    raise Exception("Run task's Exception raised!")

run_task_over()
