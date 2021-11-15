#TODO
from decoder.decode import decoder, test_path

def decode_segment(path, startindex, endindex, quality):
    return decoder(path, startindex, endindex, quality)

def test():
    test_path()
