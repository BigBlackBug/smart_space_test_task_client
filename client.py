import random
import sys
import time

import requests

SERVER_URL = "http://localhost:8080"

# SERVER_URL = "http://multiplier.bigblackbug.me:8080"

def _make_matrix(width, height, generator=lambda: random.randint(1, 10)):
    return [[generator() for i in range(width)] for j in
            range(height)]


# 'first': [[4, 2, 1], [5, 3, 6], [0, 7, 8]],
# 'second': [[9, -4], [-1, 2], [0, -2]]

print("Generating matrices")
h_1 = random.randint(10, 100)
w_1 = random.randint(10, 100)
h_2 = w_1
w_2 = random.randint(10, 100)

d_1 = (h_1, w_1)
d_2 = (h_2, w_2)
print("Submitting matrix multiplication {}x{} to {}x{}".format(*d_1, *d_2))
response = requests.post(SERVER_URL + '/multiply', json={
    'first': _make_matrix(*d_1),
    'second': _make_matrix(*d_2)
}).json()
job_id = response['job_id']
print("Job ID: {}\n".format(job_id))

while True:
    print("Polling task {}".format(job_id))
    response = requests.get(SERVER_URL + '/status/' + job_id).json()
    print("Job status: {}".format(response['status']))
    if response['status'] == 'SUCCESS':
        response = requests.get(SERVER_URL + '/result/' + job_id).json()
        print("Response: {}".format(response['result']))
        print("Bye")
        sys.exit(0)
    elif response['status'] == 'FAILURE':
        print("Job {} failed".format(job_id))
        sys.exit(0)
    time.sleep(0.5)
