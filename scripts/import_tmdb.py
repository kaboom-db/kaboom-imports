# Imports a cartoon from TMDb

import requests
import time
import json
import datetime
import var
from tmdbv3api import TMDb, TV, Season

tmdb = TMDb()
tmdb.api_key = var.TMDB_API_KEY
access_token = var.ACCESS_TOKEN
cartoons_api_url = 'http://127.0.0.1:8000/v1/cartoons/series/'
episodes_api_url = 'http://127.0.0.1:8000/v1/cartoons/episodes/'
headers = {'content-type': 'application/json', 'Authorization': 'Token ' + access_token}

tmdb_id = int(input('What is the ID of the TV show you want to import? '))

tv = TV()
cartoon = tv.details(tmdb_id)

if cartoon.status == 'Ended':
    status = 'COMPLETED'
elif cartoon.status == 'Returning Series':
    status = 'RELEASING'
elif cartoon.status == 'In Production':
    status = 'PLANNED'
else:
    status = 'CANCELLED'

cartoon_data = {
    'name': cartoon.name,
    'summary': cartoon.overview,
    'status': status,
    'season_count': cartoon.number_of_seasons,
    'tmdb_id': cartoon.id,
    'website': cartoon.homepage
}

# Check if the cartoon exists
search = requests.get(cartoons_api_url + '?query=' + cartoon.name, headers=headers)
results = search.json()['results']
res_data = {}
if not results:
    response = requests.post(cartoons_api_url, data=json.dumps(cartoon_data), headers=headers)
    print(response)
    res_data = response.json()
    print(res_data)
else:
    res_data = results[0]
    print(res_data)

# Get the seasons 
for i in range(0, cartoon.number_of_seasons):
    season = Season()
    s = season.details(cartoon.id, i + 1)
    for episode in s.episodes:
        episode_data = {
            'series': res_data['id'],
            'name': episode.name,
            'episode_number': episode.episode_number,
            'season_number': i + 1,
            'summary': episode.overview,
            'release_date': episode.air_date,
            'runtime': cartoon.episode_run_time[0] if cartoon.episode_run_time else 20
        }

        e_res = requests.post(episodes_api_url, data=json.dumps(episode_data), headers=headers)
        print(e_res)
        print(e_res.json())

        time.sleep(1)