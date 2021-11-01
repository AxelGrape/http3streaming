from mpegdash.parser import MPEGDASHParser


def parse(file_path):
    mpd_path = file_path
    return MPEGDASHParser.parse(mpd_path)


def print_data(mpd):
    for adaptation_set in mpd.periods[0].adaptation_sets:
        for representation in adaptation_set.representations:
            print("ID: {}".format(representation.id))
            print("Mime type: {}".format(representation.mime_type))
            print("Frame rate: {}".format(representation.frame_rate))
            for segment in representation.segment_templates:
                print("Init file: {}".format(segment.initialization))
                print("Media file: {}".format(segment.media))
                print("-" * 50)
    


if __name__ == '__main__':
    mpd = parse('./Encoder/var/media/hbo/dash.mpd')
    print_data(mpd)