import requests
import socket
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Safari'}
timeout = 30
socket.setdefaulttimeout(timeout)
all_datas = {
    'game': [],
    'platform': [],
    'developer': [],
    'genre': [],
    'number_players': [],
    'rating': [],
    'release_date': [],
    'metascore': [],
    'user_score': [],
}
for i in range(181):
    print('page: {}'.format(i))
    sleep(5)
    all_players = requests.get('https://www.metacritic.com/browse/games/score/metascore/all?page={}'.format(i), headers=headers)
    all_players.raise_for_status()

    all_players = BeautifulSoup(all_players.text, 'html.parser')

    all_games_name = all_players.select('h3')
    for j in all_games_name[13:113]:
        all_datas['game'].append(j.text)

    all_plateform = all_players.select('.platform .data')
    for j in all_plateform:
        all_datas['platform'].append(j.text)

    all_games_url = all_players.select('.clamp-summary-wrap .title')
    for url in all_games_url:
        if not url.select('h3'):
            continue
        print('url: {}'.format(url))
        game_info = requests.get('https://www.metacritic.com'+url['href'], headers=headers)
        game_info = BeautifulSoup(game_info.text, 'html.parser')
        info_datas = game_info.select('.data')
        all_datas['developer'].append(str(info_datas[5].text).replace('\n','').strip())
        all_datas['genre'].append(info_datas[6].text)
        all_datas['number_players'].append(info_datas[8].text)
        all_datas['rating'].append(info_datas[10].text)
        all_datas['release_date'].append(str(info_datas[1].text).replace(' ','-').replace(',-','-'))
        meta_score = game_info.select('.metascore_w span')[0].text
        all_datas['metascore'].append(meta_score)
        user_score = game_info.select('.user')[0].text
        all_datas['user_score'].append(user_score)


all_datas = pd.DataFrame(all_datas)
print(all_datas)
all_datas.to_csv('./all_games.csv', encoding='utf-8', header=False, index=False)
