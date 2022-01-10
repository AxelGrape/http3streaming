# Install
### DVAE08 - Group 1 
Will update the server specific parts more later.

## Client-side

### Install proxygen and move the client to the media player
```
cd proxygen/proxygen/
./build.sh --with-quic
cp proxygen/proxygen/_build/proxygen/httpserver/team video_player/
```

If the proxygen build fails (e.g. team does not exist after build), you can test the following:
```
cd proxygen/
./getdeps.sh
```
Try building proxygen again running getdeps.

### Install needed ubuntu libraries
```
sudo apt install ffmpeg
sudo apt-get install --reinstall libxcb-xinerama0
sudo apt-get install ubuntu-restricted-extras
```

### Install python 3.8.10 and needed libraries
Other version of python might work but has yet to be tested.
```
sudo apt-get install python3.8
sudo apt install python3-pip
pip install mpegdash
pip install PyQt5
```
# Run

### Client-side

```
cd video_player
python3 mediaPlayer.py host=130.243.27.204 (In our case)
```

### Server-side

```
proxygen/proxygen/_build/proxygen/httpserver/team --mode=server --static_root=/home/http3team/movies/ --host=130.243.27.204 (In our case)
```
