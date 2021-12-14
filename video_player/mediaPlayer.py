from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QStyle, QSizePolicy, QFileDialog, QListWidget, QGridLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
from client.client_interface import request_movie_list, request_file
from handler import RunHandler
#import threading
import sys
import os, shutil
#import time
from os.path import exists

class Window(QWidget):

    def __init__(self):
        self.full_movie_list = []
        super().__init__()

        self.setWindowTitle("Media Player")
        self.setGeometry(350, 100, 700, 500)
        self.benjamin_hanterar = None
        self.init_ui()
        self.show()

    def init_ui(self):
        # Create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlaylist = QMediaPlaylist(self.mediaPlayer)
        self.mediaPlayer.setPlaylist(self.mediaPlaylist)

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
        self.mediaPlayer.mediaChanged.connect(self.clear_playlist)
        
        # Media playlist signals
        self.mediaPlaylist.currentIndexChanged.connect(self.index_changed)

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
            #print(path.split("/")[-1])
            #file_name = path.split("/")[-1] + "/" + path.split("/")[-1] + ".mp4"
            #request_file(file_name)
            #print(f'path = {path.split("/")[-1]}')

            self.benjamin_hanterar = RunHandler(path.split("/")[-1])
            self.open_file()

            """
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
            """
            #self.remove_folders()
            #print("filmen är färdiiiig")
            #self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile()))
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
        self.fill_playlist()
        self.mediaPlayer.setMedia(QMediaContent(self.mediaPlaylist))
        self.mediaPlaylist.setCurrentIndex(0)
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


    def index_changed(self):
        self.add_media()


    def set_position(self, position):
        self.mediaPlayer.setPosition(position)


    def fill_playlist(self, slots = 2):
        for _ in range(slots):
            segment = self.benjamin_hanterar.get_next_segment()
            if segment is not False:
                media_content = QMediaContent(QUrl.fromLocalFile(os.getcwd() + "/" + segment))
                self.mediaPlaylist.addMedia(media_content)


    def clear_playlist(self):
        self.mediaPlayer.pause()
        self.mediaPlaylist.clear()


    def add_media(self):
        segment = self.benjamin_hanterar.get_next_segment()
        if segment is not False:
            media_content = QMediaContent(QUrl.fromLocalFile(os.getcwd() + "/" + segment))
            return self.mediaPlaylist.addMedia(media_content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = Window()
    player.remove_folders()
    sys.exit(app.exec_())
