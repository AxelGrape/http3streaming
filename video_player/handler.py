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
        self.mpdPath = request_file(filename)
        if(os.path.isfile(self.mpdPath)):
            print("ok")
            return self.mpdPath
        else:
            print("Bad filename")
            return False + 'Problem with downloading mpd' #prata med aksel och sitri


    #PRE: Path to downloaded .mpd file
    #POST: parser object
    def parse_mpd(self):
        try:
            self.parsedObj = MPDParser(self.mpdPath)
        except:
            print("Failed to get parser object")
            return False, "Failed to get parser object"
            
            

    #PRE: .mpd file has been parsed, got parser object, Index of current chunk(eg. 00009)
    #POST: List of next segment(s)
    def next_segment():
        print("no")

    #PRE: List of next segments
    #POST: path to next chunks(dir), Startindex, endindex, quality
    def parse_segment_list(segmentList):
        print("no")

    #PRE: path to next chunks(dir), Index of start and end chunk, quality
    #POST: path to .mp4 file
    def decode_segments(path, si, ei, q):
        success,mp4Path = decode_segment(path, si, ei, q)#(bool, pathToMp4File)
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