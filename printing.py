from cfonts import render
from os import system
from colorama import Style, Fore


def print_info(title, genre, series_info, films_info):
    logo = render('Jut su', colors=['gray', 'white'], align='left')

    system('cls')
    

    print(logo)
    print(f'Название: {title}')
    print(genre, '\n')

    season_str = 'сезон'
    seasons_name = list(series_info.keys())
    print(f'{Fore.BLACK}{Style.BRIGHT}Сезоны:{Style.RESET_ALL}')
    for i , key in enumerate(seasons_name):
        print(f'    {str(i+1)+")" if season_str not in seasons_name[0] else ""}{key}: {len(series_info[key])}', end='')
        if len(str(len(series_info[key]))) > 1 and int(str(len(series_info[key]))[-2]) == 1: 
            print(' эпизодов')
        elif int(str(len(series_info[key]))[-1]) == 1: print(' эпизод') 
        elif int(str(len(series_info[key]))[-1]) > 4 or int(str(len(series_info[key]))[-1]) == 0: print(' эпизодов') 
        else: print(' эпизода') 


    if len(films_info) != 0:
        print(f'\n{Fore.BLACK}{Style.BRIGHT}Фильмы:{Style.RESET_ALL}')
        for i in range(len(films_info)):
            print(f'    Фильм {i+1}')
    

    print(f'\n\nВведите сезон/фильм который хотите скачать:')
    print(Fore.BLACK, Style.BRIGHT, end='')
    print(f'\nПример #1: S1 (скачать первый сезон)')
    print(f'Пример #2: F2 (скачать второй фильм)')
    print(Style.RESET_ALL)

    available = ['S'+str(i) for i in range(1, len(series_info)+1)] + ['F'+str(i) for i in range(1, len(films_info)+1)]
    available = ', '.join(available)
    print(f'Доступные сезоны/фильмы: {available}\n\n')
     


    
    
    