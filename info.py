import requests
from bs4 import BeautifulSoup
import fake_useragent


headers = {
    'user-agent': fake_useragent.UserAgent().random
}

def get_url():
    return str(input('[+]Введите ссылку на аниме:\n\nПример ссылки: https://jut.su/boku-hero-academia/\n\n\n> '))


def get_info(url):
    try:
        response = requests.get(url, headers=headers)
    except:
        return 'Url Error'
    if '200' not in str(response.status_code): return 'Url Error'
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('h1', class_='header_video')
    if title == None: return 'Url Error'
    title = title.text[9:].replace(' все серии', '').replace(' и сезоны', '')
    genre = soup.find('div', class_='under_video_additional').text
    genre = genre[:genre.index('.')]
    genre = genre.replace('Аниме', '').replace('  ', ' ').replace('\n', '')
    seasons = soup.find_all('h2', class_='the-anime-season')
    series = soup.find_all('a', class_='video')
    main_info = {}


    if len(seasons) != 0 and seasons[0].text == 'Полнометражные фильмы':
        count = 0
        for i in range(len(series)-1, 0, -1):
            if 'фильм' in series[i].text:
                count += 1
            else:
                break
        main_info['1 сезон'] = [s.get('href') for s in series[:count*-1]]
        main_info['Полнометражные фильмы'] = [f.get('href') for f in series[len(series)-count:]] 

    elif len(seasons) != 0: 
        for season_tag in seasons:
            main_info[season_tag.text] = []
            next_sib = season_tag.next_sibling
            for _ in range(3):
                if next_sib.name != 'a':
                    next_sib = next_sib.next_sibling
                if next_sib.name == 'a':
                    break
            while next_sib.name == 'a':
                main_info[season_tag.text].append(next_sib.get('href'))
                next_sib = next_sib.next_sibling
                 

    elif len(seasons) == 0:
        series = soup.find_all('a', class_='short-btn')
        main_info['1 сезон'] = [s.get('href') for s in series]


    seasons_name = list(main_info.keys())
    if 'Полнометражные фильмы' in seasons_name:
        films_info = main_info['Полнометражные фильмы']
        main_info.pop('Полнометражные фильмы')
        series_info = main_info
    else:
        films_info = []
        series_info = main_info

    return title, genre, series_info, films_info


def transform(title, genre, series_info, films_info):
    season_info = (f'Название: {title}\n'+
            f'{genre[2:]}\n'+
            f'Сезоны:\n')

    season_str = 'сезон'
    seasons_name = list(series_info.keys())
    for i , key in enumerate(seasons_name):
        season_info += f'    {str(i+1)+")" if season_str not in seasons_name[0] else ""}{key}: {len(series_info[key])}'
        if len(str(len(series_info[key]))) > 1 and int(str(len(series_info[key]))[-2]) == 1: 
            season_info += ' эпизодов\n'
        elif int(str(len(series_info[key]))[-1]) == 1: season_info += ' эпизод\n'
        elif int(str(len(series_info[key]))[-1]) > 4 or int(str(len(series_info[key]))[-1]) == 0: season_info += ' эпизодов\n'
        else: season_info += ' эпизода\n'

    if len(films_info) != 0:
        season_info += '\nФильмы:\n'
        for i in range(len(films_info)):
            season_info += f'    Фильм {i+1}\n'
    return season_info


def avail(series_info, films_info):
    series_keys = [*series_info.keys()]
    for key in series_keys:
        response = requests.get('https://jut.su' + series_info[key][0], headers=headers).text
        soup = BeautifulSoup(response, 'lxml')
        if soup.find('div', class_='videoBlock').find('video') == None: series_info.pop(key)
    available = ', '.join(['S'+str(i) for i in range(1, len(series_info)+1)] + ['F'+str(i) for i in range(1, len(films_info)+1)])
    return f'Доступные сезоны/фильмы: {available}'
