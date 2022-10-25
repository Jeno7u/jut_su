from cfonts import render
from os import system
from colorama import Style, Fore
from info import get_info


def print_info():
    logo = render('Jut su', colors=['gray', 'white'], align='left')

    print(logo)
    
    title, genre, main_info = get_info()

    seasons = list(main_info.keys())
    if 'Полнометражные фильмы' in seasons:
        films_info = main_info['Полнометражные фильмы']
        main_info.pop('Полнометражные фильмы')
    else:
        films_info = []
    
    system('cls')
    
    print(logo)
    print(f'Название: {title}')
    print(genre, '\n')

    season_name = "сезон"

    print(f'{Fore.BLACK}{Style.BRIGHT}Сезоны:{Style.RESET_ALL}')
    for i in range(len(main_info)):
        print(f'    {str(i+1)+")" if season_name not in seasons[0] else ""} {seasons[i]}: {len(main_info[seasons[i]])}', end='')
        if len(str(len(main_info[seasons[i]]))) > 1 and int(str(len(main_info[seasons[i]]))[-2]) == 1: 
            print(' эпизодов')
        elif int(str(len(main_info[seasons[i]]))[-1]) == 1: print(' эпизод') 
        elif int(str(len(main_info[seasons[i]]))[-1]) > 4 or int(str(len(main_info[seasons[i]]))[-1]) == 0: print(' эпизодов') 
        else: print(' эпизода') 


    if len(films_info) != 0:
        print(f'\n{Fore.BLACK}{Style.BRIGHT}Фильмы:{Style.RESET_ALL}')
        for i in range(len(films_info)):
            print(f'    Фильм {i+1}')