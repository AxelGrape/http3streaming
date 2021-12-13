# Install
### DVAE08 - Group 1 
Will update the server specific parts more later.

## Client-side

### Install proxygen and move the client to the media player
```
proxygen/proxygen/build.sh --with-quic
cp proxygen/proxygen/_build/proxygen/httpserver/samples/team video_player/
```

### Install needed ubuntu libraries
```
sudo apt install ffmpeg
sudo apt-get install --reinstall libxcb-xinerama0
sudo apt-get install ubuntu-restricted-extras
```

### Install python 3.8.10 and needed libraries
Other version of python might work but has yet to be tested.
```
sudo apt-get install python3.8.10
python3.8.10 get-pip.py
pip install mpegdash
pip install PyQt5
```


## Server side
TODO

# Run

### Client-side

```
python3.8.10 video_player/mediaPlayer.py
```

### Server-side

```
proxygen/proxygen/_build/proxygen/httpserver/team --mode=server --static_root=/home/http3team/movies/ --host=130.243.27.204 (In our case)
```
