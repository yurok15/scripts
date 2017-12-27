import requests
import json
import math

text = 'linux'
area = 2
page = 100
page_number = 1
params = {'text': text, 'area': area, 'per_page': page, 'page': page_number}
request = requests.get('https://api.hh.ru/vacancies', params=params)
vac_number = json.loads(request.text)['found']

data = json.loads(request.text)['items']
per_page = math.ceil(vac_number / 20)
list_id = []
for vac in data:
    list_id.append(vac['id'])

print(list_id)
