import os
from parser.parse_mpd import MPDParser
from mpegdash.nodes import MPEGDASH
from decoder.decoder_interface import decode_segment
from client.client_interface import request_file, request_movie_list, custom_request
from qbuffer import QBuffer
import queue
import threading
import subprocess

class RunHandler:


    def __init__(self, filename):
        self.filename = filename
        self.mpdPath = None
        self.Qbuf = None
        self.nextSegment = None
        self.pause_cond = threading.Lock()
        self.thread = threading.Thread(target=self.queue_handler)
        #self.thread.daemon = True
        self.stop = threading.Event()
        print(self.hitIt(filename))
        self.thread.start()
        print("Init done")


    def hitIt(self,filename):
        self.mpdPath = self.request_mpd(filename)
        if not self.mpdPath: return "Error getting mpdPath in : request_mpd("+filename+")"
        tmp = self.init_Obj()
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
            self.request_all_init_files(8)
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
            self.Qbuf = queue.Queue(int(self.parsObj.get_min_buffer_time()))
            return True, ""
        except:
            print(type(self.Qbuf), type(self.parsObj), "Failed to get QBuffer object")
            return False, "Failed to get QBuffer object"


    def get_segment_length(self):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of",
                                "default=noprint_wrappers=1:nokey=1", self.nextSegment],
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT)
        return float(result.stdout)
            


    #PRE: parser object
    #POST: path to next chunks(dir), Startindex, endindex, quality
    def parse_segment(self):
        q = 0
        segment = self.parsObj.get_next_segment(q)
        print(segment[0])
        vidPath = self.mpdPath.replace("dash.mpd", "")
        try:
            index = segment[0][-9:-4]
            quality = segment[0][-11:-10]
        except:
            print("wops")

        print(index)
        print(quality)
        print(vidPath)
        print("In parse segment", self.title, index)
        request_file(f'{self.title}/{segment[0]}', vidPath)
        request_file(f'{self.title}/{segment[1]}', vidPath)

        self.nextSegment = self.decode_segments(vidPath, index, index, quality)
        self.Qbuf.put(self.nextSegment)
        



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
        newSegment = self.Qbuf.get() 
        self.thread.release()
        return newSegment

    #PRE:
    #POST:
    #decides when new segments(chunks) should be sent to videoplayer
    def queue_handler(self):
        while not self.stop.is_set():
            with self.pause_cond:
                if not self.Qbuf.full():
                    self.parse_segment()
                    print("In queue handler")
                    
                else:
                    print('Full')
                    self.pause_cond.acquire() #remember to call release in mediaplayer

        print("Queue handler exit")

    def killthread(self):
        self.stop.set()
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
