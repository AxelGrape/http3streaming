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
Number of Segments = Media Presentation Duration / Segment Duration

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


    # Return the total amounts of file chunks in the video
    def amount_of_segments(self):
        template = self.mpd.periods[0].adaptation_sets[0].representations[0].segment_templates[0]
        ss = template.segment_timelines[0].Ss
        video_duration = self.get_presentation_duration() * template.timescale
        tot = 0

        for dur in ss:
            tot += round(video_duration / dur.d)
            if dur.r is not None:
                d = dur.d * (dur.r + 1)
            else:
                d = dur.d
            video_duration -= d

        return tot


    # Helper function
    def __get_file(self, temp_file):
        chunk_number = "%05d" % self.next_segment
        _file = temp_file.replace("$Number%05d$", chunk_number)
        return _file


    # Returns the duration of a segment in seconds
    def get_segment_duration(self, segment_file: str):
        if segment_file.endswith('.m4s'):
            index = int(segment_file[-9:-4])
            repr_id = int(segment_file[-11])
        else:
            index = int(segment_file[-5::])
            repr_id = int(segment_file[-7])

        template = self.mpd.periods[0].adaptation_sets[repr_id].representations[0].segment_templates[0]
        ss = template.segment_timelines[0].Ss

        count = 0

        for i, value in enumerate(ss):
            count += 1

            if value.r != None:
                count += value.r

            if count >= index:
                return ss[i].d / template.timescale


    # Returns total video duration in seconds
    def get_presentation_duration(self):
        if self.mpd.media_presentation_duration is not None:
            return self._parse_time(self.mpd.media_presentation_duration)
        else:
            return None


    # Return max segment duration in seconds
    def get_max_segment_duration(self):
        if self.mpd.max_segment_duration is not None:
            return self._parse_time(self.mpd.max_segment_duration)
        else:
            return None


    # Returns minimum buffer time in seconds
    def get_buffer_time(self):
        if self.mpd.min_buffer_time is not None:
            return self._parse_time(self.mpd.min_buffer_time)
        else:
            return None

    
    # Return a tuple of media and audio chunks (media, audio)
    def get_next_segment(self, representation_id: int):
        segments = self.representation_chunks(representation_id)
        if segments != False:
            return segments["media"], segments["audio"]
        return False


    # Return a tuple of init files: (media, audio)
    def init_chunk(self, representation_id):
        try:
            video_adaptation = self.mpd.periods[0].adaptation_sets[representation_id]
            audio_adaptation = self.mpd.periods[0].adaptation_sets[representation_id + 1]
        except IndexError:
            print("Error: Quality {} is not available".format(representation_id))
        except:
            print("Something went wrong ;(")

        init_media = video_adaptation.representations[0].segment_templates[0].initialization.replace("$RepresentationID$", str(representation_id))
        init_audio = audio_adaptation.representations[0].segment_templates[0].initialization.replace("$RepresentationID$", str(representation_id + 1))
        return init_media, init_audio


    # Get data from a specific representation and start time (timescale format)
    # Returns a dictionary with media and audio files
    def representation_chunks(self, representation_id):
        chunks = {}
        try:
            video_adaptation = self.mpd.periods[0].adaptation_sets[representation_id]
            audio_adaptation = self.mpd.periods[0].adaptation_sets[representation_id + 1]
        except IndexError as error:
            print("Error: Quality {} is not available".format(representation_id))
        except:
            print("Something went wrong ;(")

        # Get media chunks
        for media_segment in video_adaptation.representations[0].segment_templates:
            # Get the media file name from the mpd file
            # Replace $RepresentationID$ with the actual representation id
            temp_media_file = media_segment.media.replace("$RepresentationID$", str(representation_id))

            # Replace $Number%05d$ with the correct file chunk number
            for media_timeline in media_segment.segment_timelines:
                chunks["media"] = self.__get_file(temp_media_file)


        # Get audio chunks
        for audio_segment in audio_adaptation.representations[0].segment_templates:
            # Get the media file name from the mpd file
            # Replace $RepresentationID$ with the actual representation id
            temp_audio_file = audio_segment.media.replace("$RepresentationID$", str(representation_id + 1))
            
            # Replace $Number%05d$ with the correct file chunk number
            for audio_timeline in audio_segment.segment_timelines:
                chunks["audio"] = self.__get_file(temp_audio_file)

        if self.next_segment < self.amount_of_segments() + 1:
            self.next_segment += 1
        else:
            return False
        return chunks