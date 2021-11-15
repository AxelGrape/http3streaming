from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QStyle, QSizePolicy, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
import sys

class Window(QWidget):
    def __init__(self):
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

        # Create 'Open Video' button
        openBtn = QPushButton("Open Video")
        openBtn.clicked.connect(self.open_file)

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

        # Create hbox layout
        hBoxLayout = QHBoxLayout()
        hBoxLayout.setContentsMargins(0, 0, 0, 0)

        # Set widgets to the hbox layout
        hBoxLayout.addWidget(openBtn)
        hBoxLayout.addWidget(self.playBtn)
        hBoxLayout.addWidget(self.slider)

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