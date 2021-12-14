import os
from parser.parse_mpd import MPDParser
from mpegdash.nodes import MPEGDASH
from decoder.decoder_interface import decode_segment
from client.client_interface import request_file, request_movie_list, custom_request
from time import perf_counter
#from qbuffer import QBuffer
import queue
import threading
import subprocess
import time
import math
from pathlib import Path

class RunHandler:


    def __init__(self, filename):
        self.filename = filename
        self.mpdPath = None
        self.Qbuf = None
        self.nextSegment = None
        self.newSegment = None
        self.pause_cond = threading.Lock()
        self.thread = threading.Thread(target=self.queue_handler)
        self.stop = threading.Event()
        self.throughputList = []
        print(self.hitIt(filename))
        #self.thread.start()
        print("Init done")


    def hitIt(self,filename):
        self.mpdPath = self.request_mpd(filename)
        if not self.mpdPath:
            return "Error getting mpdPath in : request_mpd("+filename+")"
        
        tmp = self.init_Obj()
        self.request_all_init_files(self.parsObj.number_of_qualities())

        if not tmp[0]:
            return tmp

        #self.parse_segment()
        #if not self.nextSegment: return "Error getting first segment"
        print("hitit done")

    #Extracts movie list content from file into a list
    #PRE: server is online
    #POST: returns a list with all available movie names
    def get_movie_list():
        movieList = []
        movieListFile = request_movie_list()
        with open(movieListFile) as file:
            while(line := file.readline().rstrip()):
                print(line)
                movieList.append(line)
        return movieList


    #request mpd file from client
    #triggered from videoplayer
    #get .mpd file back
    #PRE: Video_name
    #POST: path to downloaded .mpd file
    def request_mpd(self, filename):
        self.title = filename
        dash_path = filename + "/dash.mpd"
        dir_path = f'{os.getcwd()}/vid/{filename}'
        os.mkdir(dir_path)

        request_file(dash_path, dir_path)
        mpdPath = f'{dir_path}/dash.mpd'
        mpdPath_isfile = os.path.isfile(mpdPath)
        print(f'{mpdPath_isfile}   file is   {mpdPath}')
        if(mpdPath_isfile):
            print("MPD path exists")
            return mpdPath
        else:
            print("Bad filename")
            return False
            #return False + 'Problem with downloading mpd' #prata med aksel och sitri


    def request_all_init_files(self, quality_count):
        directory_name = self.title
        init_base_name = "dash_init_"
        file_ending = ".m4s"

        for index in range(quality_count):
            request_file(f'{directory_name}/{init_base_name}{index}{file_ending}', f'{os.getcwd()}/vid/{directory_name}')

    #PRE: Path to downloaded .mpd file
    #POST: parser object
    def init_Obj(self):
        #self.mpdPath = ''
        try:
            self.parsObj = MPDParser(self.mpdPath)
            size = int(self.parsObj.get_min_buffer_time()/2)
            if self.parsObj.amount_of_segments() < size:
                size = self.parsObj.amount_of_segments()
            self.Qbuf = queue.Queue(size)

            return True, ""
        except:
            print(type(self.Qbuf), type(self.parsObj), "Failed to get QBuffer object")
            return False, "Failed to get QBuffer object"


    def get_segment_length(self):
        return self.parsObj.get_segment_duration(self.newSegment)


    def convert_size(self, size_bytes):
       if size_bytes == 0:
           return "0B"
       size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
       i = int(math.floor(math.log(size_bytes, 1024)))
       p = math.pow(1024, i)
       s = round(size_bytes / p, 2)
       return "%s %s" % (s, size_name[i])


    #PRE: parser object
    #POST: path to next chunks(dir), Startindex, endindex, quality
    def parse_segment(self):
        q = 0
        quality_dict = self.parsObj.get_qualities()

        if len(self.throughputList) > 0:
            for quality, b in quality_dict.items():
                if self.throughputList[-1] < int(b):
                    continue
                q = quality
                break

        segment = self.parsObj.get_next_segment(q)
        print(f"Segment from parse_segment is {segment}")

        if(segment is not False):
            vidPath = self.mpdPath.replace("dash.mpd", "")
            try:
                index = segment[0][-9:-4]
                quality = segment[0][-11:-10]
            except:
                print("wops")
            t1_start = perf_counter()
            request_file(f'{self.title}/{segment[0]}', vidPath)
            t1_stop = perf_counter()
            request_file(f'{self.title}/{segment[1]}', vidPath)
            #self.throughputList.append(self.convert_size((os.path.getsize(vidPath + segment[0]))/(t1_stop - t1_start)))
            self.throughputList.append(os.path.getsize(vidPath + segment[0])/(t1_stop - t1_start))
            self.nextSegment = self.decode_segments(vidPath, index, index, quality)
        else:
            self.nextSegment = False
            self.killthread()
        return self.nextSegment
        self.Qbuf.put(self.nextSegment)


    def print_throughput(self):
        print("All throughputs :")
        for t in self.throughputList:
            print(self.convert_size(t))
        print("Latest throughput: ", self.throughputList[-1])


    #PRE: path to next chunks(dir), Index of start and end chunk, quality
    #POST: path to .mp4 file
    def decode_segments(self, path, si, ei, q):
        success,mp4Path = decode_segment(path, si, ei, q, self.title)#(bool, pathToMp4File)
        if success:
            return mp4Path
            #continue with stuff
        else:
            return False, mp4Path
            #handle fault stuff


    #Used by the videoplayer to get next .mp4 path
    def get_next_segment(self):
        #print("getting next segment")
        return self.parse_segment()
        self.newSegment = self.Qbuf.get(timeout=1)
        if not self.newSegment:
            print("get_next_segment ERROR: no newSegment")
        self.resume_thread()
        #print("self.newSegment = ", self.newSegment)
        return self.newSegment

    #PRE:
    #POST:
    #decides when new segments(chunks) should be sent to videoplayer
    def queue_handler(self):
        while not self.stop.is_set():
            with self.pause_cond:
                while not self.Qbuf.full():
                    self.parse_segment()
                    #print("In queue handler")
                self.pause_thread()

        print("Queue handler exit")


    # Return the total time currently in the queue
    def queue_time(self):
        time = 0
        q = list(self.Qbuf.queue)
        for item in q:
            if item is not False:
                time += self.parsObj.get_segment_duration(item)
        return time


    # Kill the thread. Stops filling the buffer
    def killthread(self):
        self.stop.set()
        if(self.pause_cond.locked()):
            self.pause_cond.release()
            print("Killing thread")


    def pause_thread(self, wait = 1):
        if not self.pause_cond.locked():
            self.pause_cond.acquire(timeout = wait)


    def resume_thread(self):
        if self.pause_cond.locked():
            self.pause_cond.release()




def main():
    Handler = RunHandler('nature')
    #print("hej")
    #p = MPDParser('/home/benjamin/Desktop/DVAE08/http3streaming/video_player/vid/nature/dash.mpd')
    #a = p.get_next_segment(0)
    #print(a)
    #print(p.get_segment_duration(a[0]))
    #Handler.request_mpd("nature")
    #Handler.parse_mpd()
    #Handler.parse_segment()
    #Handler.parse_segment()
    #print(Handler.get_segment_length())
    #Handler.parse_segment()

if __name__ == "__main__":
    main()
