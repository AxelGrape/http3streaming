#TODO
from decoder.decode import decoder, test_path

def decode_segment(path, startindex, endindex, quality, file_name):
    return decoder(path, startindex, endindex, quality, file_name)

def test():
    test_path()
