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
        tot = 0

        for dur in ss:
            tot += 1
            if dur.r is not None:
                tot += dur.r

        return tot


    def get_qualities(self):
        adaptations = []
        for adaptation in self.mpd.periods[0].adaptation_sets:
            adaptations.append(adaptation.id)
        return adaptations


    # Helper function
    def __get_file(self, temp_file):
        chunk_number = "%05d" % self.next_segment
        _file = temp_file.replace("$Number%05d$", chunk_number)
        return _file


    # Returns the duration of a chunk in seconds (m4s file)
    def get_segment_duration(self, file: str):
        index = int(file[-5])

        template = self.mpd.periods[0].adaptation_sets[0].representations[0].segment_templates[0]
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
    def get_min_buffer_time(self):
        if self.mpd.min_buffer_time is not None:
            return self._parse_time(self.mpd.min_buffer_time)
        else:
            return None


    # Return a tuple of media and audio chunks (media, audio)
    def get_next_segment(self, adaptation_set: int = None, bandwidth = 0):
        if adaptation_set is not None:
            segments = self.representation_chunks(adaptation_set)
            if segments != False:
                return segments["media"], segments["audio"]
            return False
        else:
            for adaptation in self.mpd.periods[0].adaptation_sets:
                if adaptation.content_type == "video":
                    for representation in adaptation.representations:
                        if bandwidth >= representation.bandwidth:
                            segments = self.representation_chunks(int(representation.id))
                            if segments is not False:
                                return segments["media"], segments["audio"]
                            return False

            segments = self.representation_chunks(int(self.mpd.periods[0].adaptation_sets[-2].id))
            if segments is not False:
                return segments["media"], segments["audio"]
            return False


    # Return a tuple of init files: (media, audio)
    def init_chunk(self, adaptation_set):
        try:
            video_adaptation = self.mpd.periods[0].adaptation_sets[adaptation_set]
            audio_adaptation = self.mpd.periods[0].adaptation_sets[adaptation_set + 1]
        except IndexError:
            print(f"Error: Qualities {adaptation_set} and {adaptation_set + 1} are not available")
            return
        except:
            print("Something went wrong ;(")
            return

        init_media = video_adaptation.representations[0].segment_templates[0].initialization.replace("$RepresentationID$", str(adaptation_set))
        init_audio = audio_adaptation.representations[0].segment_templates[0].initialization.replace("$RepresentationID$", str(adaptation_set + 1))
        return init_media, init_audio


    # Get data from a specific representation and start time (timescale format)
    # Returns a dictionary with media and audio files
    def representation_chunks(self, adaptation_set):
        chunks = {}
        print(f'Adaptation: {adaptation_set}')
        try:
            adaptation = self.mpd.periods[0].adaptation_sets[adaptation_set]
        except IndexError as error:
            print("Error: Quality {} is not available".format(adaptation_set))
            return
        except:
            print("Something went wrong ;(")
            return

        # Get media chunks
        for segment in adaptation.representations[0].segment_templates:
            # Get the media file name from the mpd file
            # Replace $RepresentationID$ with the actual representation id
            temp_media_file = segment.media.replace("$RepresentationID$", str(adaptation_set))
            temp_audio_file = segment.media.replace("$RepresentationID$", str(adaptation_set + 1))

            # Replace $Number%05d$ with the correct file chunk number
            for timeline in segment.segment_timelines:
                chunks["media"] = self.__get_file(temp_media_file)
                chunks["audio"] = self.__get_file(temp_audio_file)

        if self.next_segment < self.amount_of_segments() + 1:
            self.next_segment += 1
        else:
            return False
        return chunks
