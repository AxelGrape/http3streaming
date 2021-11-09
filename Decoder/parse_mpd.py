from mpegdash.parser import MPEGDASHParser
from re import sub
import shutil

"""

MPEGDASHParser:
    - periods
        - adaptation_sets
            - representations
                - segment_templates
                    - segment_timelines
                        - Ss
                            - t     // Timestamp of the first segment
                            - d     // Duration
                            - r     // Number of subsequent segments with the same duration


Segment Duration = Duration / Timescale
Number of Segments = mediaPresentationDuration / Segment Duration

"""

class Parser():

    def __init__(self, file_name):
        # Parse the mpd file
        self.mpd = MPEGDASHParser.parse(file_name)

        # Initiate some values
        self.buffer = []
        self.media_length = self.get_presentation_duration()
        self.max_segment_duration = self.get_segment_duration()
        self.min_buffer_time = self.get_buffer_time()


    # PTxHxMxS --> Hours:Minutes:Seconds
    # Extract total time and return in seconds
    def _parse_time(self, time):
        formatted_time = time.replace("PT", "").replace("H", ":").replace("M", ":").replace("S", "")
        temp = formatted_time.split(":")
        
        if len(temp) == 1:
            return float(temp[0])
        elif len(temp) == 2:
            return (float(temp[0]) * 60) + float(temp[1])
        elif len(temp) == 3:
            return (float(temp[0]) * 60 * 60) + (float(temp[1]) * 60) + float(temp[2])


    # Extract the file names of a representation
    def __get_media_files(self, ss, temp_file):
        media_files = []

        i = 1
        for time in ss:
            if time.r != None:
                for _ in range(time.r + 1):
                    chunk_number = "%05d" % i
                    media_files.append(temp_file.replace("$Number%05d$", chunk_number))
                    i += 1
            else:
                chunk_number = "%05d" % i
                media_files.append(temp_file.replace("$Number%05d$", chunk_number))
                i += 1
        
        return media_files


    def get_presentation_duration(self):
        if self.mpd.media_presentation_duration is not None:
            return self._parse_time(self.mpd.media_presentation_duration)
        else:
            return None


    def get_segment_duration(self):
        if self.mpd.max_segment_duration is not None:
            return self._parse_time(self.mpd.max_segment_duration)
        else:
            return None


    def get_buffer_time(self):
        if self.mpd.min_buffer_time is not None:
            return self._parse_time(self.mpd.min_buffer_time)
        else:
            return None


    def fill_buffer(self, bandwidth):
        # Fill a buffer with the segments to fill up min_buffer_time
        # Use buffer to pick next segment

        for adaptation_set in self.mpd.periods[0].adaptation_sets:
            for representation in adaptation_set.representations:
                if bandwidth >= representation.bandwidth and representation.mime_type == "video/mp4":
                    chunks = self.get_representation_chunks(int(representation.id))
                    buffer_time = 0
                    for chunk in chunks.values():
                        for index, media_chunk in enumerate(chunk[1]):
                            if buffer_time < self.min_buffer_time:
                                self.buffer.append(media_chunk)
                                buffer_time += representation.segment_templates[0].segment_timelines[0].Ss[index].d / representation.segment_templates[0].timescale
                    return


    def get_next_segment(self):
        # TO DO:
        # Return the next segment
        return 0


    # Get data from a specific representation
    def get_representation_chunks(self, representation_id):
        mpd_data = {}

        for representation in self.mpd.periods[0].adaptation_sets[representation_id].representations:
            for segment in representation.segment_templates:
                # Get the init file name and media file name from the mpd file
                # Replace $RepresentationID$ with the actual representation id
                init_file = segment.initialization.replace("$RepresentationID$", representation.id)
                temp_media_file = segment.media.replace("$RepresentationID$", representation.id)
                
                # Replace $Number%05d$ with the correct file chunk number
                for timeline in segment.segment_timelines:
                    media_files = self.__get_media_files(timeline.Ss, temp_media_file)
            
            mpd_data[representation_id] = [init_file, media_files]
        return mpd_data


    # Get data from all the representations
    def get_all_chunks(self):
        mpd_data = {}

        for adaptation_set in self.mpd.periods[0].adaptation_sets:
            for representation in adaptation_set.representations:
                for segment in representation.segment_templates:
                    # Get the init file name and media file name from the mpd file
                    # Replace $RepresentationID$ with the actual representation id
                    init_file = segment.initialization.replace("$RepresentationID$", representation.id)
                    temp_media_file = segment.media.replace("$RepresentationID$", representation.id)

                    # Replace $Number%05d$ with the correct file chunk number
                    for timeline in segment.segment_timelines:
                        media_files = self.__get_media_files(timeline.Ss, temp_media_file)

            mpd_data[representation.id] = [init_file, media_files]

        return mpd_data


if __name__ == '__main__':
    parser = Parser('./../Encoder/var/media/SampleVideo_1280x720_10mb/dash.mpd')
    chunks = parser.get_all_chunks()
    parser.fill_buffer(500000)
    #mpd = parse_mpd('./../Encoder/var/media/SampleVideo_1280x720_10mb/dash.mpd')
    #mpd_data = parser.get_all_files(mpd)
    #print(mpd_data)