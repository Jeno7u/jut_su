def progress_bar(current, total, bar_length=20):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    ending = '\n' if int(fraction*100) == 100 else '\r'

    print(f'Прогресс: [{arrow}{padding}] {int(fraction*100)}%', end=ending)