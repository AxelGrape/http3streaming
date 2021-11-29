import threading
import time
from parser.parse_mpd import MPDParser

"""
class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.paused = False
        self.pause_cond = threading.Thread(threading.Lock())

    
    def run(self):
        print("Starting")
        while True:
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()
                
                print("Fill buffer")
        print("Ending")
    

    def pause(self):
        self.paused = True
        self.pause_cond.acquire()


    def resume(self):
        self.paused = False
        self.pause_cond.notify()
        self.pause_cond.release()
"""

class QBuffer():

    def __init__(self, mpd):
        self.buffer = []
        self.mpd = mpd


    def buffer_time(self):
        sum = 0
        for i in range(len(self.buffer)):
            t = self.mpd.get_segment_duration(self.buffer[i][0])
            sum += t

        return sum


    def fill_buffer(self, adaptation_set, pause_cond):
        min_buffer_time = self.mpd.get_buffer_time()
        while True:
            with pause_cond:
                while self.buffer_time() < min_buffer_time:
                    self.buffer.append(self.mpd.get_next_segment(adaptation_set))
                print("Buffer: {}".format(qbuf.buffer))
                print("Pause thread")
                pause_cond.acquire()
                print("Continue thread")
        
        print("Exiting thread")


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
        except IndexError as error:
            print("Error: {}".format(error))
        except:
            print("Error: Something went wrong")


if __name__ == '__main__':
    parser = MPDParser('./vid/nature/dash.mpd')
    qbuf = QBuffer(parser)
    pause_cond = threading.Lock()

    thread = threading.Thread(target=qbuf.fill_buffer, args=(0, pause_cond))
    thread.start()
    
    qbuf.remove_segment()
    pause_cond.release()
    thread.join()
    print("Exiting main thread")