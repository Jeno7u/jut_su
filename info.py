import requests
from bs4 import BeautifulSoup
import fake_useragent


headers = {
    'user-agent': fake_useragent.UserAgent().random
}


def get_info():
    url = str(input('[+]Введите ссылку на аниме:\n\nПример ссылки: https://jut.su/horimiya/\n\n\n> '))

    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    title = soup.find('h1', class_='header_video').text[9:].replace(' все серии', '').replace(' и сезоны', '')
    genre = soup.find('div', class_='under_video_additional').text
    if 'Темы' in genre: genre = genre[:genre.index('Темы')]
    else: genre = genre[:genre.index('Тема')]
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
        print(main_info)

    elif len(seasons) != 0: 
        for season_tag in seasons:
            main_info[season_tag.text] = []
            next_sib = season_tag.next_sibling
            while next_sib.name == 'a':
                main_info[season_tag.text].append(next_sib.get('href'))
                next_sib = next_sib.next_sibling

    elif len(seasons) == 0:
        series = soup.find_all('a', class_='short-btn')
        main_info['1 сезон'] = [s.get('href') for s in series]


    return title, genre, main_info