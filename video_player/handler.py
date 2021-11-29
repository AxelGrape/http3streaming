import os
from decoder.decoder_interface import decode_segment
from client.client_interface import request_file, request_movie_list, custom_request
from parser.parse_mpd import MPDParser

class RunHandler:


    def __init__(self):
        self.title = None
        self.mpdPath = None
        self.parsedObj = None
        print("no")

    def hitIt(self):
        self.request_mpd()
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
        dash_path = self.title + "/dash.mpd"
        os.mkdir(f'{os.getcwd()}/vid/{filename}')
        part_of_mpd_path = request_file(dash_path, f'{os.getcwd()}/vid/{filename}')
        self.mpdPath = f'{part_of_mpd_path}/dash.mpd'
        print(f'{os.path.isfile(self.mpdPath)}   file is   {self.mpdPath}')
        if(os.path.isfile(self.mpdPath)):
            print("ok")
            self.request_all_init_files(8)
            return self.mpdPath
        else:
            print("Bad filename")
            #return False + 'Problem with downloading mpd' #prata med aksel och sitri

    def request_all_init_files(self, quality_count):
        directory_name = self.title
        init_base_name = "dash_init_"
        file_ending = ".m4s"

        for index in range(quality_count):
            request_file(f'{directory_name}/{init_base_name}{index}{file_ending}', f'{os.getcwd()}/vid/{directory_name}')

    #PRE: Path to downloaded .mpd file
    #POST: parser object
    def parse_mpd(self):
        #self.mpdPath = ''
        try:
            self.parsedObj = MPDParser(self.mpdPath)
        except:
            print("Failed to get parser object")
            return False, "Failed to get parser object"





    #PRE: parser object
    #POST: path to next chunks(dir), Startindex, endindex, quality
    def parse_segment(self):
        q = 0
        segment = self.parsedObj.get_next_segment(q)
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
    #Handler.parse_segment()

if __name__ == "__main__":
    main()
