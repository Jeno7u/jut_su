from numpy import choose
import requests
from bs4 import BeautifulSoup
import fake_useragent
from extra import progress_bar
from os import system


headers = {
    'user-agent': fake_useragent.UserAgent().random
}

def choose_resolution(url):
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    video_tag = soup.find('video')
    sources = video_tag.find_all('source')
    resolutions = [src.get('res')+'p' for src in sources]

    system('cls')
    
    print('\n[+]Доступные к скачиванию разрешения:  ', end='')
    print(', '.join(resolutions))
    resolution = str(input('[+]Введите разрешение скачеваемого видео из предложенных:  '))
    
    return resolution


def download_video(url, resolution):
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    video_title = soup.find('div', class_='vpt_roll').text
    print(video_title)
    video_tag = soup.find('video')

    video_link = video_tag.find('source', {'res': resolution}).get('src')
    video_headers = requests.head(video_link, headers=headers)
    video_len = int(video_headers.headers['content-length'])/1024//1024
    video = requests.get(video_link, headers=headers, stream=True)
    series_count = url.split('-')[-1].split('.')[0]


    print(f'[+]Начало скачивания "{video_title} (Эпизод {series_count}).mp4"')

    with open(f'{video_title} (Эпизод {series_count}).mp4', 'wb') as file:
        count_mb = 0
        for chunk in video.iter_content(chunk_size=1024*1024):
            if chunk:
                progress_bar(count_mb, video_len)
                count_mb += 1
                file.write(chunk)
    
    print('[+]Скачивание прошло успешно!')



def download_videos(title, genre, series_info, films_info):
    series_keys = list(series_info.keys())
    whichDownload = str(input(' >')).upper()

    if whichDownload[0] == 'S':
        season_to_download = series_info[series_keys[1]]
        from_series = int(input(f'С какой серии скачивать (Максимум: {len(season_to_download)}): '))
        to_series = int(input(f'По какую серию скачивать (Максимум: {len(season_to_download)}): '))
        series_to_download = season_to_download[from_series-1:to_series-1]
        for series_url in series_to_download:
            url = 'https://jut.su/'+series_url
            download_video(url, choose_resolution(url))
    

