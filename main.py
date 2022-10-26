from printing import print_info
from info import get_info
from download import download_videos


def main():
    info = get_info()
    print_info(*info)
    download_videos(*info)

if __name__ == '__main__':
    main()