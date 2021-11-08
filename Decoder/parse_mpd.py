from mpegdash.parser import MPEGDASHParser
from string import Template
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


Segment Duration = Duration + Timescale
Number of Segments = mediaPresentationDuration ÷ Segment Duration

"""


# Extract the file names of a representation
def get_media_files(ss, temp_file):
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

# PTxHxMxS --> Hours:Minutes:Seconds
# Extract total time and return in seconds
def parse_time(time):
    formatted_time = time.replace("PT", "").replace("H", ":").replace("M", ":").replace("S", "")
    temp = formatted_time.split(":")
    
    if len(temp) == 1:
        return float(temp[0])
    elif len(temp) == 2:
        return (float(temp[0]) * 60) + float(temp[1])
    elif len(temp) == 3:
        return (float(temp[0]) * 60 * 60) + (float(temp[1]) * 60) + float(temp[2])


def get_presentation_duration(mpd):
    return parse_time(mpd.media_presentation_duration)


def get_segment_duration(mpd):
    return parse_time(mpd.max_segment_duration)


def get_buffer_time(mpd):
    return parse_time(mpd.min_buffer_time)


# Get data from a specific representation
def extract_representation_data(mpd, representation_id):
    mpd_data = {}

    for representation in mpd.periods[0].adaptation_sets[representation_id].representations:
        for segment in representation.segment_templates:
            # Get the init file name and media file name from the mpd file
            # Replace $RepresentationID$ with the actual representation id
            init_file = segment.initialization.replace("$RepresentationID$", representation.id)
            temp_media_file = segment.media.replace("$RepresentationID$", representation.id)
            
            # Replace $Number%05d$ with the correct file chunk number
            for timeline in segment.segment_timelines:
                media_files = get_media_files(timeline.Ss, temp_media_file)
        
        mpd_data[representation_id] = [init_file, media_files]
    return mpd_data


# Get data from all the representations
def extract_all_data(mpd):
    mpd_data = {}

    for adaptation_set in mpd.periods[0].adaptation_sets:
        for representation in adaptation_set.representations:
            for segment in representation.segment_templates:
                # Get the init file name and media file name from the mpd file
                # Replace $RepresentationID$ with the actual representation id
                init_file = segment.initialization.replace("$RepresentationID$", representation.id)
                temp_media_file = segment.media.replace("$RepresentationID$", representation.id)
                
                # Replace $Number%05d$ with the correct file chunk number
                for timeline in segment.segment_timelines:
                    media_files = get_media_files(timeline.Ss, temp_media_file)

        mpd_data[representation.id] = [init_file, media_files]

    return mpd_data
    



# ---- Test function ----
def print_data(mpd):
    total_duration = float(sub("[^0.0-9.0]", "", mpd.media_presentation_duration))
    print("Total video duration: {}".format(total_duration))

    for representation in mpd.periods[0].adaptation_sets[0].representations:
        for segment in representation.segment_templates:
            init_file = segment.initialization.replace("$RepresentationID$", representation.id)
            temp_media_file = segment.media.replace("$RepresentationID$", representation.id)

            segment_timescale = segment.timescale
            for timeline in segment.segment_timelines:
                media_files = get_media_files(timeline.Ss, temp_media_file)
            
            print("Init file: {}".format(init_file))
            print("Media files: {}".format(media_files))
            print("-" * 50)


if __name__ == '__main__':
    mpd = MPEGDASHParser.parse('./../Encoder/var/media/sample_video/dash.mpd')
    #mpd_data = extract_all_data(mpd)
    #print(mpd_data)