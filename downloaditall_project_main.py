import os
import sys
import requests
import urllib

from pytube import YouTube
from downloaditall import Ui_MainWindow

from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui
import re

# from downloaditall_project_main import browseFiles, clickDownload, provideURL, fileProgress


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle('downloaditall')
        self.browseButton.clicked.connect(self.browseFiles)
        self.videoTitle
        self.selectVideoQualityBox
        self.downloadButton.clicked.connect(self.clickDownload)
        # self.downloadButton.clicked.connect(self.fileProgress)
        self.progressBar.setMaximum(100)
        self.URLBar
        self.checkURL.clicked.connect(self.provideURL)

    def browseFiles(self):

        # path = os.path.join('', )
        self.filename = QFileDialog.getExistingDirectory(
            self, 'Save File')
        if self.filename:
            self.destinationBar.setText(str(self.filename))

    def provideURL(self, audio_only=False):
        self.yt = YouTube(self.URLBar.text())
        if self.yt:
            self.streams = self.yt.streams
            link = str(self.URLBar.text())
            self.YouTubeURL = YouTube(link)
            self.videoTitle.setText(self.YouTubeURL.title)
            pixmap = QPixmap()
            pixmap.loadFromData(urllib.request.urlopen(
                self.YouTubeURL.thumbnail_url).read())
            self.pictureLabel.setPixmap(pixmap)
            pixmap.scaled(400, 225, Qt.KeepAspectRatio,
                          Qt.FastTransformation)

            for stream in self.streams:
                self.streams.order_by('resolution')
                self.selectVideoQualityBox.addItem(str(stream))

    def clickDownload(self):
        selection = (self.selectVideoQualityBox.currentText())
        itag = re.findall(r'itag="(.*?)"', selection)[0]
        print(itag)
        # self.yt.register_on_progress_callback(self.fileProgress)
        file = self.streams.get_by_itag(itag)
        file.download(output_path=self.filename)

    # def fileProgress(self, totalSize, stream=None, chunk=None, remaining=None):
    #     fileSize = self.stream.filesize
    #     self.progressBar.setValue(100 * (fileSize - remaining)) / fileSize
    #     QApplication.processEvents()


if __name__ == '__main__':
    app = qtw.QApplication([])
    app.setStyle('Fusion')
    window = Window()
    window.show()

    sys.exit(app.exec_())
