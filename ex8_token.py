import time

import requests

url = 'https://playground.learnqa.ru/ajax/api/longtime_job'


def result(num, text, status_code):
    print(f'{num} \n'
          f'text = {text} \n'
          f'status_code = {status_code}')


response_start = requests.get(url)
result('# start', response_start.text, response_start.status_code)

token = response_start.json()['token']
seconds = response_start.json()['seconds']

response_status = requests.get(url, params={"token": token})
status = response_status.json()['status']
assert status == 'Job is NOT ready'
result('# status', response_status.text, response_status.status_code)

time.sleep(seconds)

response_result = requests.get(url, params={"token": token})
status_result = response_result.json()['status']
assert status_result == 'Job is ready'
result('# result', response_result.text, response_result.status_code)

if 'result' in response_result.json():
    print(f"result = {response_result.json()['result']}")
else:
    print(f"'result' в JSON нет")
