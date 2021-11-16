from mpegdash.parser import MPEGDASHParser

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

class MPDParser():

    def __init__(self, file_path):
        self.mpd = MPEGDASHParser.parse(file_path)
        self.next_segment = 1


    # PTxHxMxS --> Hours:Minutes:Seconds
    # Returns the time in seconds
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
    # Start: index of the first file
    # Duration: amount of seconds that should be retrieved
    def __get_file(self, ss, temp_file):
        chunk_number = "%05d" % self.next_segment
        _file = temp_file.replace("$Number%05d$", chunk_number)
        return _file


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

    def get_next_segment(self, representation_id):
        chunks = self.get_representation_chunks(representation_id)
        return chunks["media"], chunks["audio"]


    # Return a tuple of init files: (media, audio)
    def get_init_chunk(self, representation_id):
        video_adaptation = self.mpd.periods[0].adaptation_sets[representation_id]
        audio_adaptation = self.mpd.periods[0].adaptation_sets[representation_id + 1]

        init_media = video_adaptation.representations[0].segment_templates[0].initialization.replace("$RepresentationID$", str(representation_id))
        init_audio = audio_adaptation.representations[0].segment_templates[0].initialization.replace("$RepresentationID$", str(representation_id + 1))
        return init_media, init_audio


    # Get data from a specific representation and start time (timescale format)
    # Returns a dictionary with media and audio files
    def get_representation_chunks(self, representation_id, duration = 10):
        chunks = {}
        video_adaptation = self.mpd.periods[0].adaptation_sets[representation_id]
        audio_adaptation = self.mpd.periods[0].adaptation_sets[representation_id + 1]

        # Get media chunks
        for segment in video_adaptation.representations[0].segment_templates:
            # Get the media file name from the mpd file
            # Replace $RepresentationID$ with the actual representation id
            temp_media_file = segment.media.replace("$RepresentationID$", str(representation_id))

            # Replace $Number%05d$ with the correct file chunk number
            for timeline in segment.segment_timelines:
                chunks["media"] = self.__get_file(timeline.Ss, temp_media_file)

        # Get audio chunks
        for segment in audio_adaptation.representations[0].segment_templates:
            # Get the media file name from the mpd file
            # Replace $RepresentationID$ with the actual representation id
            temp_audio_file = segment.media.replace("$RepresentationID$", str(representation_id + 1))
            
            # Replace $Number%05d$ with the correct file chunk number
            for timeline in segment.segment_timelines:
                chunks["audio"] = self.__get_file(timeline.Ss, temp_audio_file)

        self.next_segment += 1
        return chunks


if __name__ == '__main__':
    parser = MPDParser('./../Encoder/var/media/SampleVideo/dash.mpd')
    media_segment, audio_segment = parser.get_next_segment(0)
    print("Segment 1: {}, {}".format(media_segment, audio_segment))
    media_segment, audio_segment = parser.get_next_segment(0)
    print("Segment 2: {}, {}".format(media_segment, audio_segment))
    media_segment, audio_segment = parser.get_next_segment(0)
    print("Segment 3: {}, {}".format(media_segment, audio_segment))