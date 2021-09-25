import os
import sys
import requests
import urllib

from pytube import YouTube
from downloaditallUi import Ui_MainWindow

from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui
import re
import ffmpeg

# from downloaditall_project_main import browseFiles, clickDownload, provideURL, fileProgress


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle('downloaditall')
        self.browseButton.clicked.connect(self.browseFiles)
        self.videoTitle
        self.selectVideoQualityBox
        self.progressBar.setMaximum(100)
        self.URLBar
        self.checkURL.clicked.connect(self.provideURL)
        self.downloadButton.clicked.connect(self.clickDownload)
        self.downloadButton.clicked.connect(self.combineVideoandAudio)

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
            self.linkString = str(self.URLBar.text())
            self.YouTubeURL = YouTube(self.linkString)
            self.videoTitle.setText(self.YouTubeURL.title)
            pixmap = QPixmap()
            pixmap.loadFromData(urllib.request.urlopen(
                self.YouTubeURL.thumbnail_url).read())
            self.pictureLabel.setPixmap(pixmap)
            pixmap.scaled(384, 216, Qt.KeepAspectRatio,
                          Qt.FastTransformation)

            for stream in self.streams:
                self.streams.filter(file_extension='mp4')
                # self.streams.order_by('resolution')
                self.selectVideoQualityBox.addItem(str(stream))

    def clickDownload(self):
        selection = (self.selectVideoQualityBox.currentText())
        itag = re.findall(r'itag="(.*?)"', selection)[0]
        print(itag)
        # self.streams.register_on_progress_callback(self.fileProgress)
        videoFile = self.streams.get_by_itag(itag)
        videoFile.download(output_path=f'{self.filename}')

        audioFile = self.streams.get_audio_only()
        audioOutput = audioFile.download(
            output_path=self.filename, filename=f'{self.YouTubeURL.title}_audio.mp4')

    def combineVideoandAudio(self):

        print(
            f'Directory: {self.filename} \nFilename {self.YouTubeURL.title}.mp4, \nComplete Path: {self.filename}/{self.YouTubeURL.title}.mp4 ')

        try:
            videoStream = ffmpeg.input(
                f'{self.filename}/{self.YouTubeURL.title}.mp4')
            audioStream = ffmpeg.input(
                f'{self.filename}/{self.YouTubeURL.title}_audio.mp4')
            ffmpeg.output(audioStream, videoStream,
                          f'{self.YouTubeURL.title}1.mp4').run(capture_stdout=True, capture_stderr=True)
        except ffmpeg._run.Error as e:
            print("fatal error: ", file=sys.stderr)
            print('stdout:', e.stdout)
            print('stderr:', e.stderr)
            raise e

        print('project complete')

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
