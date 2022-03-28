# Imports a comic from Comicvine

import requests
import json
import time
import var
from simyan.session import Session

comicvine = Session(var.COMICVINE_API_KEY)
access_token = var.ACCESS_TOKEN
comics_api_url = 'http://127.0.0.1:8000/v1/comics/series/'
issues_api_url = 'http://127.0.0.1:8000/v1/comics/issues/'
headers = {'content-type': 'application/json', 'Authorization': 'Token ' + access_token}
statuses = ['COMPLETED', 'RELEASING', 'PLANNED', 'CANCELLED']

cv_id = input('What is the ID of the volume you want to import? ')
for i in range(len(statuses)) : print(f'({i}) {statuses[i]}')
status = -1
while status < 0 or status > len(statuses) - 1:
    status = int(input('Which status does this comic correspond to (enter the number): '))

comic = comicvine.volume(_id=cv_id)

comic_data = {
    'series_name': f'{comic.name} ({comic.start_year})',
    'summary': comic.summary if comic.summary else 'Temp',
    'year_started': comic.start_year,
    'status': statuses[status]
}

# Check if the comic exists
search = requests.get(comics_api_url + '?query=' + f'{comic.name} ({comic.start_year})', headers=headers)
results = search.json()['results']
res_data = {}
if not results:
    response = requests.post(comics_api_url, data=json.dumps(comic_data), headers=headers)
    print(response)
    res_data = response.json()
    print(res_data)
else:
    res_data = results[0]
    print(res_data)

for i in range(len(comic.issues)):
    issue_data = {
        'series_id': res_data['id'],
        'issue_name': comic.issues[i].name if comic.issues[i].name else f'{comic.name} ({i + 1})',
        'issue_number_absolute': i + 1,
        'format_id': 1
    }
    if len(issue_data['issue_name']) > 200:
        print('Issue name too long... defaulting...')
        issue_data['issue_name'] = f'{comic.name} ({i + 1})'

    i_res = requests.post(issues_api_url, data=json.dumps(issue_data), headers=headers)
    print(issue_data)
    print(i_res)
    print(i_res.json())

    time.sleep(1)