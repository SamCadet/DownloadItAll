import os
import sys
import urllib
from pytube import YouTube
from downloaditallUi import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets as qtw
import re
import ffmpeg
import subprocess

# from downloaditall_project_main import browseFiles, clickDownload, provideURL, fileProgress


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle('downloaditall')
        self.browseButton.clicked.connect(self.browseFiles)
        self.videoTitle.setWordWrap(True)
        self.selectVideoQualityBox
        self.progressBar.setMaximum(100)
        self.URLBar
        self.checkURL.clicked.connect(self.provideURL)
        self.downloadButton.clicked.connect(self.clickDownload)
        self.downloadButton.clicked.connect(self.combineVideoandAudio)

    def provideURL(self, audio_only=False):
        self.progressBar.setValue(0)
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
            # pixmap.scaled(1920, 1080, Qt.KeepAspectRatio,
            #               Qt.FastTransformation)

            for stream in self.streams.filter(file_extension='mp4', adaptive=True).order_by('resolution'):

                self.selectVideoQualityBox.addItem(str(stream))

    def removeReservedChars(self, youTubeURL):

        reservedChars = {'<', '>', ':', '"',
                         '/', '\\', '|', '?', '*', '[', ']'}

        for char in youTubeURL:
            if char in reservedChars:
                youTubeURL = youTubeURL.replace(char, '_')

        return youTubeURL

    def browseFiles(self):

        self.newYouTubeTitle = self.removeReservedChars(self.YouTubeURL.title)

        self.filename = QFileDialog.getExistingDirectory(
            self, 'Save File')
        if self.filename:

            self.destinationBar.setText(
                f'{self.filename}/{self.newYouTubeTitle}')

    def clickDownload(self):

        self.selection = (self.selectVideoQualityBox.currentText())
        itag = re.findall(r'itag="(.*?)"', self.selection)[0]
        videoFile = self.streams.get_by_itag(itag)
        videoFile.download(output_path=self.filename,
                           filename=f'{self.newYouTubeTitle}_video.mp4')

        self.yt.register_on_progress_callback(self.fileProgress)

        audioFile = self.streams.get_audio_only()
        audioFile.download(output_path=self.filename,
                           filename=f'{self.newYouTubeTitle}_audio.mp4')

    def combineVideoandAudio(self):

        fullPathVideo = f'"{self.filename}/{self.newYouTubeTitle}_video.mp4"'
        fullPathAudio = f'"{self.filename}/{self.newYouTubeTitle}_audio.mp4"'
        outputFile = f'"{self.filename}/{self.newYouTubeTitle}.mp4"'
        codec = 'copy'

        # videoStream = ffmpeg.input(fullPathVideo)
        # audioStream = ffmpeg.input(fullPathAudio)
        # ffmpeg.output(videoStream, audioStream,
        #               outputFile, vcodec=codec).run(capture_stdout=True, capture_stderr=True)

        createFile = subprocess.run(
            f'ffmpeg -i {fullPathVideo} -i {fullPathAudio} -c:v libx264 -preset veryfast -c:a {codec} {outputFile}')

        os.remove(f'{self.newYouTubeTitle}_video.mp4')
        os.remove(f'{self.newYouTubeTitle}_audio.mp4')

        print(createFile.stdout)

    def fileProgress(self, stream, chunk, bytes_remaining):
        size = stream.filesize
        progress = int((abs(bytes_remaining - size) / size)) * 100
        self.progressBar.setValue(progress)


if __name__ == '__main__':
    app = qtw.QApplication([])
    app.setStyle('Fusion')
    window = Window()
    window.show()

    sys.exit(app.exec_())
