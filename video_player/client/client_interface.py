from client.client_comm import get_request
import os

#Usage:
#import interface.py and use one of these functions, do not import client_comm
#Requires that you move ./hq from proxygen httpserver samples into the /python_interface/ folder

#Pre: a file name, e.g. "hello.txt"
#Post: True or false if the file was able to be downloaded or not
def request_file(file_name, storage_path, host):
    get_request(file_name, storage_path, host)

#Post: List of all available movies
def request_movie_list(storage_path, host):
    get_request("list_movies", storage_path, host)
