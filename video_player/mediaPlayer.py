from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QStyle, QSizePolicy, QFileDialog, QListWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
from client.client_interface import request_movie_list, request_file
import sys

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
        videoWidget = QVideoWidget()

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
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create Listbox
        self.listwidget = QListWidget()
        self.refresh_movie_list()
        for i, movie in enumerate(self.full_movie_list):
            self.listwidget.insertItem(i, movie)
        self.listwidget.clicked.connect(self.clicked)

        # Create hbox layout
        hBoxLayout = QHBoxLayout()
        hBoxLayout.setContentsMargins(0, 0, 0, 0)

        # Set widgets to the hbox layout


        hBoxLayout.addWidget(self.listwidget)
        hBoxLayout.addWidget(self.playBtn)
        hBoxLayout.addWidget(self.slider)
        hBoxLayout.addWidget(self.refreshBtn)
        hBoxLayout.addWidget(self.selectMovieBtn)

        # Create vbox layout
        vBoxLayout = QVBoxLayout()
        vBoxLayout.addWidget(videoWidget)
        vBoxLayout.addWidget(self.label)
        vBoxLayout.addLayout(hBoxLayout)

        self.setLayout(vBoxLayout)
        self.mediaPlayer.setVideoOutput(videoWidget)

        # Media player signals
        self.mediaPlayer.stateChanged.connect(self.state_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    # When a movie have been "clicked"
    def clicked (self, qmodelindex):
        item = self.listwidget.currentItem()
        #print(item.text())

    def request_movie(self):
        item = self.listwidget.currentItem()
        if item is None:
            print("You most choose a movie from the list")
        else:
            path = item.text()
            print(path.split("/")[-1])
            file_name = path.split("/")[-1] + "/" + path.split("/")[-1] + ".mp4"
            print(file_name)
            request_file(file_name)

    def refresh_movie_list(self):
        pathy = request_movie_list()
        with open(pathy) as f:
            lines = f.read().splitlines()
            print(lines)
        self.full_movie_list = lines
        print(lines)
        print("TODO")

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
