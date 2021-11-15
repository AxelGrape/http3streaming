import os

#Post: Returns false if a given file has content, otherwise true
def empty_file(file_name):
    return os.stat(file_name).st_size == 0

#Post: Returns true if a given file has content, otherwise deletes the file
def control_file(file_name):
    if(empty_file(file_name)):
        os.remove("file_name")
        return False
    else:
        return True
