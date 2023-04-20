import sys
from PyQt5.QtWidgets import QApplication
from init_gui import Window


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
    

if __name__ == '__main__':
    main()