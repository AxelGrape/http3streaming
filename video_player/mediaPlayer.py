from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QStyle, QSizePolicy, QFileDialog, QListWidget, QGridLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
from client.client_interface import request_movie_list, request_file
from handler import RunHandler
import sys
import os, shutil
import time
from os.path import exists

class Window(QWidget):

    def __init__(self):
        self.full_movie_list = []
        super().__init__()

        self.setWindowTitle("Media Player")
        self.setGeometry(350, 100, 700, 500)

        self.init_ui()
        self.show()

    def init_ui(self):
        # Create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Create video widget object
        self.videoWidget = QVideoWidget()

        # Create 'Refresh' button
        self.refreshBtn = QPushButton("Refresh list")
        self.refreshBtn.clicked.connect(self.refresh_movie_list)

        # Create 'Select Video' button
        self.selectMovieBtn = QPushButton("Select movie")
        self.selectMovieBtn.clicked.connect(self.request_movie)

        # Create 'Play' button
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        # Create 'Slider'
        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.set_position)

        # Create a label
        #self.label = QLabel("tjo")
        #self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create Listbox
        self.listwidget = QListWidget()
        self.refresh_movie_list()

        #for i, movie in enumerate(self.full_movie_list):
            #self.listwidget.insertItem(i, movie)
        #self.listwidget.clicked.connect(self.clicked)

        layout = QGridLayout()

        layout.addWidget(self.listwidget, 0, 0, 1, 2)
        layout.addWidget(self.videoWidget, 0, 3, 1, 7)
        #layout.addWidget(self.label, 1, 0)
        layout.addWidget(self.playBtn, 1, 3)
        layout.addWidget(self.slider, 1, 4,)
        layout.addWidget(self.refreshBtn, 1, 0)
        layout.addWidget(self.selectMovieBtn, 1, 1)


        self.setLayout(layout)
        self.mediaPlayer.setVideoOutput(self.videoWidget)

        # Media player signals
        self.mediaPlayer.stateChanged.connect(self.state_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    # When a movie have been "clicked"
    #def clicked (self, qmodelindex):
    #    item = self.listwidget.currentItem()
        #print(item.text())


    def remove_folders(self):
        folder = os.getcwd() + '/vid/'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


    def request_movie(self):
        item = self.listwidget.currentItem()
        if item is None:
            print("You must choose a movie from the list")
        else:
            self.remove_folders()
            path = item.text()
            print(path.split("/")[-1])
            file_name = path.split("/")[-1] + "/" + path.split("/")[-1] + ".mp4"
            #request_file(file_name)
            print(f'path = {path.split("/")[-1]}')
            benjamin_hanterar = RunHandler(path.split("/")[-1])


            movie_active = True

            while(movie_active):
                segment = benjamin_hanterar.get_next_segment()
                if(segment is False):
                    movie_active = False
                    benjamin_hanterar.print_throughput()
                    break
                else:
                    #print("segment is ", segment)
                    self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(os.getcwd() + "/" + segment)))
                    self.mediaPlayer.play()
                    time.sleep(benjamin_hanterar.get_segment_length())

            self.remove_folders()
            print("filmen är färdiiiig")
            #self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile()))
            #self.mediaPlayer.play()

#
            #benjamin_hanterar = RunHandler()
            #self.playBtn.setEnabled(True)
            #benjamin_hanterar.request_mpd(path.split("/")[-1])
            #benjamin_hanterar.parse_mpd()
            #benjamin_hanterar.parse_segment()
            #self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("/home/axel/Documents/School/HT2021/DVAE08/http3streaming/video_player/vid/nature/out/vid00001.mp4")))
            #self.mediaPlayer.play()
            #benjamin_hanterar.parse_segment()
            #time.sleep(benjamin_hanterar.get_segment_length())
            #self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("/home/axel/Documents/School/HT2021/DVAE08/http3streaming/video_player/vid/nature/out/vid00002.mp4")))
            #self.mediaPlayer.play()
            #benjamin_hanterar.parse_segment()
            #time.sleep(benjamin_hanterar.get_segment_length())
            #self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("/home/axel/Documents/School/HT2021/DVAE08/http3streaming/video_player/vid/nature/out/vid00003.mp4")))
            #self.mediaPlayer.play()

    def update_list_widget(self):
        self.listwidget.clear()
        for i, movie in enumerate(self.full_movie_list):
            self.listwidget.insertItem(i, movie)

    def refresh_movie_list(self):
        pathy = os.getcwd() + "/list_movies"
        request_movie_list(os.getcwd())

        if(os.path.isfile(pathy)):
            if(exists(pathy)):
                if(os.stat("list_movies").st_size != 0):
                    with open(pathy) as f:
                        lines = f.read().splitlines()
                        print(lines)
                    self.full_movie_list = lines
            self.update_list_widget()
            os.remove(pathy)

    def open_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if fileName != "":
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playBtn.setEnabled(True)


    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def state_changed(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, time):
        self.slider.setValue(time)


    def duration_changed(self, duration):
        self.slider.setRange(0, duration)


    def set_position(self, position):
        self.mediaPlayer.setPosition(position)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = Window()
    sys.exit(app.exec_())
