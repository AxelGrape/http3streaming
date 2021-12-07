import threading
import sys
#import time
from parser.parse_mpd import MPDParser


class QBuffer():

    def __init__(self, mpd_file):
        self.buffer = []
        self.mpd = MPDParser(mpd_file)
        self.pause_cond = threading.Lock()
        self.kill = threading.Event()

        self.thread = threading.Thread(target=self.fill_buffer, args=(0,))
        self.thread.start()

    
    # Returns the current amount of time in the buffer (in seconds)
    def current_buffer_time(self):
        sum = 0
        for i in range(len(self.buffer)):
            sum += self.mpd.get_segment_duration(self.buffer[i][0])

        return sum


    # Used by the thread to keep the buffer filled
    def fill_buffer(self, adaptation_set):
        min_buffer_time = self.mpd.get_buffer_time()
        while not self.kill.is_set():
            with self.pause_cond:
                while self.current_buffer_time() < min_buffer_time:
                    s = self.mpd.get_next_segment(adaptation_set)
                    if s:
                        self.buffer.append(s)
                    else:
                        break
                self.pause_cond.acquire()

    
    # Return the next segment from the buffer and removes it from the buffer
    def next_segment(self):
        try:
            s = self.buffer.pop(0)
            self.pause_cond.release()
            return s
        except IndexError:
            print("Error: Buffer is empty")
            return False

    
    # Return the duration of a segment
    # Takes the name or the index of the segment as input
    def segment_duration(self, segment):
        if type(semgnet) == str:
            return self.mpd.get_segment_duration(segment)
        elif type(segment) == int:
            try:
                return self.mpd.get_segment_duration(self.buffer[segment][0])
            except IndexError as e:
                print("Error: {}".format(e))


    # Appends a segment to the buffer (append a media file and an audio file as a tuple)
    def add_segment(self, segment):
        self.buffer.append(segment)


    # Removes a segment from the buffer. Can take the index of a segment or the file name of a segment
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


    # Kills the thread, stops filling the buffer
    def end_thread(self):
        self.kill.set()
        self.pause_cond.release()
        print("Exiting thread")

"""
if __name__ == '__main__':
    qbuf = QBuffer('../server/Encoder/var/media/nature/dash.mpd')
    
    for x in range(40):
        print(f"Buffer: {qbuf.buffer}")
        print(f"Next segment: {qbuf.next_segment()}")
        print("-"*50)
        time.sleep(.01)

    qbuf.end_thread()

    if qbuf.kill.is_set():
        qbuf.thread.join()
        print("Exiting main thread")
        sys.exit()
"""