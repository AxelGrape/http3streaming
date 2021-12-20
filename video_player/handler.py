import os
from parser.parse_mpd import MPDParser
from mpegdash.nodes import MPEGDASH
from decoder.decoder_interface import decode_segment
from client.client_interface import request_file, request_movie_list, custom_request
from time import perf_counter
from quality.quality_handler import student_entrypoint
#from qbuffer import QBuffer
import queue
import threading
import subprocess
import time
import math
from pathlib import Path
import logging
from datetime import datetime

class RunHandler:


    def __init__(self, filename):
        self.filename = filename
        self.mpdPath = None
        self.Qbuf = None
        self.nextSegment = None
        self.newSegment = None
        self.rebuffCount = 0
        self.quality_changes = 0
        self.latest_quality = 0
        self.used_qualities = []
        self.pause_cond = threading.Lock()
        self.thread = threading.Thread(target=self.queue_handler, daemon=True)
        self.stop = threading.Event()
        self.throughputList = []
        print(self.hitIt(filename))
        self.thread.start()
        print("Init done")


    def hitIt(self,filename):
        self.mpdPath = self.request_mpd(filename)
        if not self.mpdPath: return "Error getting mpdPath in : request_mpd("+filename+")"
        tmp = self.init_Obj()
        self.request_all_init_files(self.parsObj.number_of_qualities())
        logging.basicConfig(filename="log/" + self.log_name_generator(filename),
                                    filemode='a',
                                    format='%(asctime)s,%(msecs)d %(levelname)s %(message)s',
                                    datefmt='%H:%M:%S',
                                    level=logging.DEBUG)
        if not tmp[0]: return tmp
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

    def log_name_generator(self, filename):
        now = datetime.now()

        print("now =", now)
        dt_string = now.strftime("%d%m%Ytime%H:%M:%S")
        return filename+dt_string

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

        """
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of",
                                "default=noprint_wrappers=1:nokey=1", self.newSegment],
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT)
        return float(result.stdout)
        """

    def convert_size(self, size_bytes):
       if size_bytes == 0:
           return "0B"
       size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
       i = int(math.floor(math.log(size_bytes, 1024)))
       p = math.pow(1024, i)
       s = round(size_bytes / p, 2)
       return "%s %s" % (s, size_name[i])

    #Measured_Bandwidth, Buffer_Occupancy, Available_Bitrates, Rebuffering_Time
    def quality_calculator(self):
        q = 6
        quality_dictionary = self.parsObj.get_qualities()
        if(len(self.throughputList) > 0):
            print("Habtes kod : ", student_entrypoint(self.throughputList[-1] * 8, self.queue_time(), quality_dictionary, 0))


        if(len(self.throughputList) > 0):
            for quality, b in quality_dictionary.items():
                quality_set = False
                if int(self.throughputList[-1]) > int(b):
                    quality_set = True
                    q = quality
                    break
            if(quality_set is False):
                q = max(quality_dictionary.keys())
        if q is not self.latest_quality:
            self.quality_changes += 1
            if q in self.used_qualities:
                logging.info(f'QUALITY_CHANGE {self.latest_quality:} -> {q}')
                logger = logging.getLogger(f'urbanGUI')
            else:
                logging.info(f'QUALITY_CHANGE {self.latest_quality:} -> {q} (NEW QUALITY)')
                logger = logging.getLogger(f'urbanGUI')
                self.used_qualities.append(q)
        self.latest_quality = q
        return q

    #PRE: parser object
    #POST: path to next chunks(dir), Startindex, endindex, quality
    def parse_segment(self):
        q = 6
        if(len(self.throughputList) > 0):
            q = student_entrypoint(self.throughputList[-1]* 8, self.queue_time(), self.parsObj.get_qualities(), self.rebuffCount)
            self.rebuffCount = 0


        if q is not self.latest_quality:
            self.quality_changes += 1
            if q in self.used_qualities:
                logging.info(f'QUALITY_CHANGE {self.latest_quality:} -> {q}')
                logger = logging.getLogger(f'urbanGUI')
            else:
                logging.info(f'QUALITY_CHANGE {self.latest_quality:} -> {q} (NEW QUALITY)')
                logger = logging.getLogger(f'urbanGUI')
                self.used_qualities.append(q)
        self.latest_quality = q

        segment = self.parsObj.get_next_segment(q)
        print("Segment from parse_segment is ", segment)
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
            self.throughputList.append(round(os.path.getsize(vidPath + segment[0])/(t1_stop - t1_start)))
            logging.info(f'THROUGHPUT {self.throughputList[-1]} B/s')
            logger = logging.getLogger(f'urbanGUI')
            self.nextSegment = self.decode_segments(vidPath, index, index, quality)
        else:
            self.nextSegment = False
            self.killthread()

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
        if success :
            return mp4Path
            #continue with stuff
        else:
            return False, mp4Path
            #handle fault stuff


    #Used by the videoplayer to get next .mp4 path
    def get_next_segment(self):
        print("getting next segment")
        self.newSegment = self.Qbuf.get()
        if not self.newSegment:
            print("get_next_segment ERROR: no newSegment")
        if self.pause_cond.locked():
            print("lock locked, releasing lock")
            self.pause_cond.release()
        print("self.newSegment = ", self.newSegment)
        if(len(self.Qbuf.queue) < 1):
            self.rebuffCount +=1
            logging.info(f'REBUFFERING {self.newSegment}')
            logger = logging.getLogger(f'urbanGUI')
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
                self.pause_cond.acquire()

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
            print("killing thread")




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
