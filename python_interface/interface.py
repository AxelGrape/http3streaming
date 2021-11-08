import client_comm

#Usage:
#import interface.py and use one of these functions, do not import client_comm


#Pre: a file name, e.g. "hello.txt"
#Post: True or false if the file was able to be downloaded or not
def request_file(file_name):
    return get_request(file_name)
