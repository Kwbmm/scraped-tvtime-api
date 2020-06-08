from typing import Dict, List
from bs4 import BeautifulSoup
import requests
import Utils


def check_data(params: Dict[str, str]) -> bool:
    if not Utils.are_form_data_keys_valid(params, ['symfony', 'tvstRemember', 'user_id']):
        return False
    return Utils.are_form_data_values_valid(params)


def get_shows(params: Dict[str, str]) -> Dict[str, any]:
    cookies = {'symfony': params['symfony'], 'tvstRemember': params['tvstRemember']}
    resp = requests.get("https://www.tvtime.com/en/user/{}/profile".format(params['user_id']), cookies=cookies,
                        headers=Utils.HEADERS)
    resp.raise_for_status()
    series = __parse_series(resp.text)
    return {'series': series, 'count': len(series)}


def __parse_series(shows_page: str) -> List[any]:
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
