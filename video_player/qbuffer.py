import threading
import sys
import time
from parser.parse_mpd import MPDParser


class QBuffer():

    def __init__(self, mpd):
        self.buffer = []
        self.mpd = mpd
        self.pause_cond = threading.Lock()
        self.kill = threading.Event()

        self.thread = threading.Thread(target=self.fill_buffer, args=(0,))
        self.thread.start()


    def current_buffer_time(self):
        sum = 0
        for i in range(len(self.buffer)):
            t = self.mpd.get_segment_duration(self.buffer[i][0])
            sum += t

        return sum


    def fill_buffer(self, adaptation_set):
        print("-"*50)
        min_buffer_time = self.mpd.get_buffer_time()
        while not self.kill.is_set():
            with self.pause_cond:
                while self.current_buffer_time() < min_buffer_time:
                    self.buffer.append(self.mpd.get_next_segment(adaptation_set))
                print("Buffer: {}".format(self.buffer))
                print("Pause thread")
                self.pause_cond.acquire()
                print("-"*50)
                print("Continue thread")


    def add_segment(self, segment):
        self.buffer.append(segment)


    def remove_segment(self, segment = None):
        try:
            if type(segment) == int:
                    del self.buffer[segment]
            else:
                if segment == None:
                    del self.buffer[0]
                elif segment != None:
                    self.buffer.remove(segment)
            self.pause_cond.release()
        except IndexError as error:
            print("Error: {}".format(error))
        except:
            print("Error: Something went wrong")


    def end_thread(self):
        self.kill.set()
        self.pause_cond.release()
        print("Exiting thread")


if __name__ == '__main__':
    parser = MPDParser('../server/Encoder/var/media/nature/dash.mpd')
    qbuf = QBuffer(parser)
    
    print("Remove segment")
    qbuf.remove_segment()
    time.sleep(2)
    qbuf.end_thread()

    if qbuf.kill.is_set():
        qbuf.thread.join()
        print("Exiting main thread")
        sys.exit()
    