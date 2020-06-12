from typing import Dict, List, Any
from bs4 import BeautifulSoup
from flask import session

import requests
import Config
import Utils


def get_shows() -> Dict[str, any]:
    resp = requests.get("https://www.tvtime.com/en/user/{}/profile".format(session['username']['user_id']),
                        cookies=Utils.get_tvtime_cookies(),
                        headers=Config.HEADERS)
    resp.raise_for_status()
    Utils.update_tvtime_cookies(resp.cookies)
    series = parse_series_list(resp.text)
    return {'series': series, 'count': len(series)}


def parse_series_list(shows_page: str) -> List[any]:
    parser = BeautifulSoup(shows_page, 'html.parser')
    series = list()
    for element in parser.select('div#all-shows ul.shows-list.posters-list div.show'):
        show_name = element.select_one('div.poster-details > h2 > a').text.strip()
        if show_name == '':
            continue
        show_id = element.select_one('a.show-link')['href'].split('/')[3]
        progress = element.select_one('a.show-link div.progress-bar')['style'].split(':')[1].strip()
        time = element.select_one('div.poster-details > h3').text.strip()
        series.append({'id': show_id, 'progress': progress, 'name': show_name, 'time': time})
    return series


def get_show(show_id: int) -> Dict[str, Any]:
    resp = requests.get('https://www.tvtime.com/en/show/{}'.format(show_id), headers=Config.HEADERS,
                        cookies=Utils.get_tvtime_cookies())
    resp.raise_for_status()
    Utils.update_tvtime_cookies(resp.cookies)
    seasons = parse_season_list(resp.text)
    return {"count": len(seasons), "seasons": seasons}


def parse_season_list(show_page: str) -> List[Any]:
    parser = BeautifulSoup(show_page, 'html.parser')
    seasons = list()
    for season_element in parser.select("div#show-seasons > div.seasons > div.season-content"):
        season_name = season_element.select_one("span[itemprop='name']").text.strip()
        num_episodes = season_element.select_one("span[itemprop='numberOfEpisodes']").text.strip()
        episodes = list()
        for episode_element in season_element.select("ul.episode-list > li.episode-wrapper > div.infos > div.row"):
            episode_id = episode_element.select_one('a')['href'].split('/')[5]
            episode_number = episode_element.select_one('span.episode-nb-label').text.strip()
            episode_name = episode_element.select_one('span.episode-name').text.strip()
            episode_air_date = episode_element.select_one('span.episode-air-date').text.strip()
            episodes.append(
                {"id": episode_id, "number": episode_number, "name": episode_name, "air_date": episode_air_date})
        seasons.append({"name": season_name, "number_of_episodes": num_episodes, "episodes": episodes})
    return seasons
