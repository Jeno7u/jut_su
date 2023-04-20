import requests
from bs4 import BeautifulSoup
import fake_useragent
import os

from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication


headers = {
    'user-agent': fake_useragent.UserAgent().random
}


def progress_bar(current, total, bar_length=20):
    fraction = current/total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    return f'Прогресс: [{arrow}{padding}] {int(fraction*100)}%'


def choose_resolution(url):
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    video_tag = soup.find('video')
    sources = video_tag.find_all('source')
    return [src.get('res')+'p' for src in sources]

    
        
class DownloadThread(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, args):
        super().__init__()

        self.args = args
        self.downloading_info = ''
    
    def emit_signal(self):
        self.update_signal.emit(self.downloading_info)
        self.msleep(20)
        QApplication.processEvents()

    def run(self):
        self.download_videos(*self.args)
    
    #download videos that you choose 
    def download_videos(self, title, genre, series_info, films_info, whichDownload, series_from, series_to, resolution, dir_):
        series_keys = list(series_info.keys())
        title = title.replace(' ', '_')

        if whichDownload[0] == 'S':
            season_to_download = series_info[series_keys[int(whichDownload[1])-1]]
            series_to_download = season_to_download[series_from-1:series_to]
            for series_url in series_to_download:
                url = 'https://jut.su'+series_url
                print('start downloading video')
                self.download_video(url, title, resolution, whichDownload, dir_)
        
        if whichDownload[0] == 'F':
            url = 'https://jut.su'+films_info[int(whichDownload[1])-1]
            self.download_video(url, title, resolution, whichDownload, dir_)
    
    #download specified video
    def download_video(self, url, title, resolution, whichDownload, dir_):
        #getting page html
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, 'lxml')

        #video info
        video_title = soup.find('div', class_='video_plate_title').text
        video_tag = soup.find('video')
        video_link = video_tag.find('source', {'res': resolution}).get('src')
        video_headers = requests.head(video_link, headers=headers)
        video_len = int(video_headers.headers['content-length'])/1024//1024-1
        video = requests.get(video_link, headers=headers, stream=True)

        #preparing for downloading
        series_count = url.split('-')[-1].split('.')[0]
        dir_name = f'{title} ({whichDownload}) ({resolution}p)'
        down_text = 'Эпизод' if whichDownload[0] == 'S' else 'Фильм'
        remove = '/\:*?<>|'
        for rem in remove:
            video_title = video_title.replace(rem, ' ')
        

        #text updating
        self.downloading_info += f'[+]Начало скачивания "{video_title} ({down_text} {series_count}).mp4"\n'
        self.emit_signal()

        #creating folder 
        if not os.path.exists(dir_ + '/' + dir_name):
            os.mkdir(dir_ + '/' + dir_name)

        #downloading
        count_mb = 0
        with open(f'{dir_}/{dir_name}/{video_title} ({down_text} {series_count}).mp4', 'wb') as file:
            for chunk in video.iter_content(chunk_size=1024*1024):
                if chunk:
                    if count_mb != 0 and count_mb <= video_len:
                        self.downloading_info = self.downloading_info.replace(progress_bar(count_mb-1, video_len), '')
                    
                    if count_mb <= video_len:
                        self.downloading_info += progress_bar(count_mb, video_len)
                        self.emit_signal()
                        
                        count_mb += 1

                    file.write(chunk)

            self.downloading_info += '\n\n'

