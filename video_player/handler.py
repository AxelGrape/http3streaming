from decoder.decoder_interface import decode_segment


class RunHandler:
    def __init__(self, title):
        self.title = title
        print("no")

    def hitIt(self):
        self.request_mpd()
        print("no")
        
    
    def get_movie_list():
        print("no")
    #request mpd file from client
    #triggered from videoplayer
    #get .mpd file back
    #PRE: Video_name
    #POST: path to downloaded .mpd file
    def request_mpd():
        print("no")

    #PRE: Path to downloaded .mpd file
    #POST: parser object
    def parse_mpd():
        print("no")

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