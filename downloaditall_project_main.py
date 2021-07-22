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
        self.downloadButton.clicked.connect(self.fileProgress)
        self.progressBar.setMaximum(100)
        self.URLBar
        self.checkURL.clicked.connect(self.provideURL)

    def browseFiles(self):
        global filename
        path = os.path.join('', )
        filename = QFileDialog.getExistingDirectory(
            self, 'Save File')
        if filename:
            self.destinationBar.setText(str(filename))

    def provideURL(self, audio_only=False):
        global yt
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

            for stream in self.streams.all():
                self.streams.order_by('resolution')
                self.selectVideoQualityBox.addItem(str(stream))

    def clickDownload(self):
        self.yt = YouTube(self.URLBar.text())
        self.streams = self.yt.streams
        itag = self.selectVideoQualityBox.itemData(
            self.selectVideoQualityBox.currentIndex())
        self.yt.register_on_progress_callback(self.fileProgress)
        self.streams.download(output_path=filename, itag=itag)

    def fileProgress(self, totalSize, stream=None, chunk=None, remaining=None):
        fileSize = stream.filesize
        self.progressBar.setValue(100 * (fileSize - remaining)) / fileSize
        # QApplication.processEvents()


if __name__ == '__main__':
    app = qtw.QApplication([])
    app.setStyle('Fusion')
    window = Window()
    window.show()

    sys.exit(app.exec_())
