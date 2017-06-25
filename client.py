# SERVER_URL = "http://multiplier.bigblackbug.me:8080"
import os
import time

import requests

SERVER_URL = os.environ.get("SERVER_URL", "http://localhost:8080")


def multiply(first, second):
    print("Sending multiplication request")
    response = requests.post(SERVER_URL + '/multiply', json={
        'first': first,
        'second': second
    }).json()
    return response['job_id']


def poll(job_id, sleep_time=0.5):
    while True:
        print("Polling task {}".format(job_id))
        response = requests.get(
            "{}/status/{}".format(SERVER_URL, job_id)).json()
        print("Job status: {}".format(response['status']))
        if response['status'] == 'SUCCESS':
            response = requests.get(
                "{}/result/{}".format(SERVER_URL, job_id)).json()
            print("Response: {}".format(response['result']))
            break
        elif response['status'] == 'FAILURE':
            print("Job {} failed".format(job_id))
            break
        time.sleep(sleep_time)
