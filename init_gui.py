import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QEventLoop
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QScrollArea, QMessageBox, QComboBox, QFrame, QFileDialog, QVBoxLayout
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QFont

from info import get_info, transform, avail
from download import choose_resolution, DownloadThread


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.lenght = 530
        self.width = 340
        self.title = "JutSu"
        self.widgets = []

        self.resize(self.lenght, self.width)
        self.setWindowTitle(self.title)

        self.init_url_frame()

    # creating error
    def create_error(self, text):
        error = QMessageBox()
        error.setWindowTitle("Ошибка")
        error.setText(text)
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()

    # getting url of anime
    def init_url_frame(self):
        self.label = QLabel("Введите ссылку на аниме", self)
        self.label.setGeometry(QtCore.QRect(20, 110, 221, 31))
        font = QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.widgets.append(self.label)

        self.lineEdit_url = QLineEdit(self)
        self.lineEdit_url.setGeometry(QtCore.QRect(20, 160, 351, 25))
        self.lineEdit_url.setPlaceholderText(
            "https://jut.su/boku-hero-academia/")
        self.widgets.append(self.lineEdit_url)

        self.btn = QPushButton("Готово", self)
        self.btn.setGeometry(QtCore.QRect(387, 157, 120, 32))
        self.btn.clicked.connect(self.get_data)
        self.widgets.append(self.btn)

    # based on writed url getting main data
    def get_data(self):
        self.url = self.lineEdit_url.text()
        self.data = get_info(self.url)
        if self.data == 'Url Error':
            self.create_error(
                "Проверьте правильность ссылки или качество работы интернета!")
        else:
            self.data_info = transform(*self.data)
            print(self.data_info)
            self.available = avail(*self.data[2:])
            print(self.available)

            self.change_frame_info()

    # changing frame to info
    def change_frame_info(self):
        for widget in self.widgets:
            widget.hide()
            widget = None
        self.widgets = []

        self.init_info_frame()

    # printing info about anime
    def init_info_frame(self):
        self.label_info = QLabel(self.data_info, self)
        self.label_info.setAlignment(Qt.AlignLeft)
        self.label_info.setStyleSheet("margin-top: 5;"
                                      "margin-left: 5")
        self.widgets.append(self.label_info)
        self.label_info.show()

        self.scrollArea_info = QScrollArea(self)
        self.scrollArea_info.setGeometry(QtCore.QRect(10, 46, 441, 181))
        self.scrollArea_info.setWidgetResizable(True)
        self.scrollArea_info.setWidget(self.label_info)
        self.widgets.append(self.scrollArea_info)
        self.scrollArea_info.show()

        self.label_top = QLabel("Информация об аниме", self)
        self.label_top.setGeometry(QtCore.QRect(20, 11, 191, 21))
        font = QFont()
        font.setPointSize(16)
        self.label_top.setFont(font)
        self.widgets.append(self.label_top)
        self.label_top.show()

        self.lineEdit_available = QLineEdit(self)
        self.lineEdit_available.setPlaceholderText("Пример: S2")
        self.lineEdit_available.setGeometry(QtCore.QRect(190, 299, 141, 21))
        self.widgets.append(self.lineEdit_available)
        self.lineEdit_available.show()

        self.btn = QPushButton("Готово", self)
        self.btn.setGeometry(QtCore.QRect(334, 294, 113, 32))
        self.btn.clicked.connect(self.change_frame_down_info)
        self.widgets.append(self.btn)
        self.btn.show()

        self.label_available = QLabel(self.available, self)
        self.label_available.setStyleSheet("margin-left: 5")
        self.widgets.append(self.label_available)
        self.label_available.show()

        self.scrollArea_available = QScrollArea(self)
        self.scrollArea_available.setGeometry(QtCore.QRect(10, 236, 441, 51))
        self.scrollArea_available.setWidgetResizable(True)
        self.scrollArea_available.setWidget(self.label_available)
        self.widgets.append(self.scrollArea_available)
        self.scrollArea_available.show()

        self.label_below = QLabel("Выберите сезон/фильм", self)
        self.label_below.setGeometry(QtCore.QRect(19, 300, 171, 16))
        font = QFont()
        font.setPointSize(14)
        self.label_below.setFont(font)
        self.widgets.append(self.label_below)
        self.label_below.show()

    # changing frame to down_info frame
    def change_frame_down_info(self):
        self.which_download = self.lineEdit_available.text().upper()

        if self.which_download not in self.available:
            self.create_error("Данный сезон недоступен")
            return

        for widget in self.widgets:
            widget.hide()
            widget = None
        self.widgets = []

        self.season_to_download = [
            *self.data[2].keys()][int(self.which_download[1])-1]
        self.resolutions = choose_resolution(
            'https://jut.su/' + self.data[2][self.season_to_download][0])
        self.init_down_info_frame()

    # getting info for downloading videos

    def init_down_info_frame(self):
        self.label_top = QLabel("Введите информацию о скачиваемом видео", self)
        self.label_top.move(15, 30)
        font = QFont()
        font.setPointSize(16)
        self.label_top.setFont(font)
        self.label_top.adjustSize()
        self.widgets.append(self.label_top)
        self.label_top.show()

        font = QFont()
        font.setPointSize(15)

        self.label_from = QLabel("С какой серии скачивать", self)
        self.label_from.move(26, 80)
        self.label_from.setFont(font)
        self.label_from.adjustSize()
        self.widgets.append(self.label_from)
        self.label_from.show()

        self.lineEdit_from = QLineEdit(self)
        if self.which_download[0] == "F":
            self.lineEdit_from.setEnabled(False)
            self.lineEdit_from.setPlaceholderText(
                "У фильма нельзя выбрать серии")
        else:
            self.lineEdit_from.setPlaceholderText(
                f"Максимум {len(self.data[2][self.season_to_download])}")
        self.lineEdit_from.setGeometry(QtCore.QRect(270, 80, 113, 21))
        self.widgets.append(self.lineEdit_from)
        self.lineEdit_from.show()

        self.label_to = QLabel("По какую серию скачивать", self)
        self.label_to.move(26, 120)
        self.label_to.setFont(font)
        self.label_to.adjustSize()
        self.widgets.append(self.label_to)
        self.label_to.show()

        self.lineEdit_to = QLineEdit(self)
        if self.which_download[0] == "F":
            self.lineEdit_to.setEnabled(False)
            self.lineEdit_to.setPlaceholderText(
                "У фильма нельзя выбрать серии")
        else:
            self.lineEdit_to.setPlaceholderText(
                f"Максимум {len(self.data[2][self.season_to_download])}")
        self.lineEdit_to.setGeometry(QtCore.QRect(270, 120, 113, 21))
        self.widgets.append(self.lineEdit_to)
        self.lineEdit_to.show()

        self.label_res = QLabel("Выберите разрешение видео", self)
        self.label_res.move(26, 182)
        self.label_res.setFont(font)
        self.label_res.adjustSize()
        self.widgets.append(self.label_res)
        self.label_res.show()

        self.comboBox_res = QComboBox(self)
        for i in range(len(self.resolutions)):
            self.comboBox_res.addItem(str(self.resolutions[i]))
        self.comboBox_res.setGeometry(QtCore.QRect(270, 180, 118, 26))
        self.widgets.append(self.comboBox_res)
        self.comboBox_res.show()

        self.label_folder = QLabel("Выберите папку для скачивания", self)
        self.label_folder.move(26, 232)
        self.label_folder.setFont(font)
        self.label_folder.adjustSize()
        self.widgets.append(self.label_folder)
        self.label_folder.show()

        self.btn_folder = QPushButton("Открыть папку", self)
        self.btn_folder.setGeometry(QtCore.QRect(266, 226, 124, 32))
        self.btn_folder.clicked.connect(self.open_folder)
        self.widgets.append(self.btn_folder)
        self.btn_folder.show()

        self.btn = QPushButton("Готово", self)
        self.btn.setGeometry(QtCore.QRect(20, 290, 124, 32))
        self.btn.clicked.connect(self.change_down_frame)
        self.widgets.append(self.btn)
        self.btn.show()

    # getting directory to save file
    def open_folder(self):
        self.dir_ = QFileDialog.getExistingDirectory(
            None, 'Select project folder:', 'C:\\', QFileDialog.ShowDirsOnly)

    # changing frame to downloading frame
    def change_down_frame(self):
        if self.which_download[0] == "S":
            try:
                self.serie_from = int(self.lineEdit_from.text())
                self.serie_to = int(self.lineEdit_to.text())
            except:
                self.create_error(
                    "Ошибка  в поле выбора серий! Проверьте правильность введенных данных!")
                return
        else:
            self.serie_from = -1
            self.serie_to = -1
        self.resolution = self.comboBox_res.currentText()[:-1]

        if self.serie_from == "" or self.serie_to == "" or self.dir_ == None:
            self.create_error("Не все данные были введены!")
            return

        for widget in self.widgets:
            widget.hide()
            widget = None
        self.widgets = []

        self.init_down_frame()

    # downloading choosed series/film
    def init_down_frame(self):
        self.label = QLabel("Загрузка", self)
        self.label.setGeometry(QtCore.QRect(20, 30, 81, 19))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.show()

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setGeometry(QtCore.QRect(30, 70, 401, 241))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.show()
        self.content = QtWidgets.QWidget()
        self.content.setGeometry(QtCore.QRect(0, 0, 429, 239))
        self.content.show()

        self.label_downloading = QLabel("", self.content)
        self.label_downloading.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_downloading.show()

        self.verticalLayout = QVBoxLayout(self.content)
        self.verticalLayout.addWidget(self.label_downloading)
        self.scrollArea.setWidget(self.content)

        self.init_downloading_videos()

    def init_downloading_videos(self):
        download_thread = DownloadThread(
            (*self.data, self.which_download, self.serie_from, self.serie_to, self.resolution, self.dir_,))
        download_thread.update_signal.connect(self.update_label_text)
        download_thread.start()
        loop = QEventLoop()
        loop.exec_()
        download_thread.wait()

    def update_label_text(self, text):
        self.label_downloading.setText(text)
