import requests
from bs4 import BeautifulSoup
import fake_useragent
from extra import progress_bar


headers = {
    'user-agent': fake_useragent.UserAgent().random
}


def download_video(url):
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    video_title = soup.find('span', {'itemprop': 'name'}).text
    video_title = video_title.replace('Смотреть ', '').replace(' ', '_')
    video_tag = soup.find('video')
    sources = video_tag.find_all('source')
    resolutions = [src.get('res')+'p' for src in sources]

    print('[+]Доступные к скачиванию разрешения:  ', end='')
    print(', '.join(resolutions))
    resolution = str(input('[+]Введите разрешение скачеваемого видео из предложенных:  '))

    video_link = video_tag.find('source', {'res': resolution}).get('src')
    video_headers = requests.head(video_link, headers=headers)
    video_len = int(video_headers.headers['content-length'])/1024//1024
    video = requests.get(video_link, headers=headers, stream=True)


    print(f'[+]Начало скачивания "{video_title}.mp4"')

    with open(f'{video_title}.mp4', 'wb') as file:
        count_mb = 0

        for chunk in video.iter_content(chunk_size=1024*1024):
            if chunk:
                progress_bar(count_mb, video_len)
                count_mb += 1

                file.write(chunk)
    
    print('[+]Скачивание прошло успешно!')
