import os
from decoder.decoder_interface import decode_segment
from client.client_interface import request_file, request_movie_list, custom_request
from qbuffer import QBuffer

class RunHandler:


    def __init__(self, filename):
        self.filename = filename
        self.mpdPath = None
        self.Qbuf = None
        self.nextSegment = None
        self.hitIt(filename)
        print("no")


    def hitIt(self,filename):
        self.mpdPath = self.request_mpd(filename)
        if self.mpdPath == False:
            return "Error getting mpdPath in : request_mpd("+filename+")"
        self.init_QBuffer()
        self.parse_segment()
        self.parse_segment()
        print(self.get_segment_length())
        print("no")

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
            print("ok")
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
    def init_QBuffer(self):
        #self.mpdPath = ''
        try:
            self.Qbuf = QBuffer(self.mpdPath)
        except:
            print("Failed to get QBuffer object")
            return False, "Failed to get QBuffer object"


    def get_segment_length(self):
        return self.parsedObj.get_segment_duration(self.nextSegment)


    #PRE: parser object
    #POST: path to next chunks(dir), Startindex, endindex, quality
    def parse_segment(self):
        q = 0
        segment = self.Qbuf.next_segment(q)
        self.nextSegment = segment[0]
        print(self.nextSegment)
        vidPath = self.mpdPath.replace("dash.mpd", "")
        try:
            index = segment[0][-9:-4]
            quality = segment[0][-11:-10]
        except:
            print("wops")

        print(index)
        print(quality)
        print(vidPath)
        print("no")
        request_file(f'{self.title}/{segment[0]}', vidPath)
        request_file(f'{self.title}/{segment[1]}', vidPath)

        self.decode_segments(vidPath, index, index, quality)



    #PRE: path to next chunks(dir), Index of start and end chunk, quality
    #POST: path to .mp4 file
    def decode_segments(self, path, si, ei, q):
        success,mp4Path = decode_segment(path, si, ei, q, self.title)#(bool, pathToMp4File)
        if success :
            print("Path is: " + mp4Path)
            #continue with stuff
        else:
            print("Error: " + mp4Path)
            #handle fault stuff


    #PRE:
    #POST:
    #decides when new segments(chunks) should be sent to videoplayer
    def queue_handler():
        print("no")



def main():
    Handler = RunHandler()
    #print("hej")
    #p = MPDParser('/home/benjamin/Desktop/DVAE08/http3streaming/video_player/vid/nature/dash.mpd')
    #a = p.get_next_segment(0)
    #print(a)
    #print(p.get_segment_duration(a[0]))
    Handler.request_mpd("nature")
    Handler.parse_mpd()
    Handler.parse_segment()
    Handler.parse_segment()
    print(Handler.get_segment_length())
    #Handler.parse_segment()

if __name__ == "__main__":
    main()
