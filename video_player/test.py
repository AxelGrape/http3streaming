from qbuffer import QBuffer
from parser.parse_mpd import MPDParser

if __name__ == '__main__':
    parser = MPDParser('./vid/nature/dash.mpd')
    qbuf = QBuffer(parser)
    print("Bufer time: {}".format(qbuf.buffer_time()))