import client_comm

#Usage:
#import interface.py and use one of these functions, do not import client_comm
#Requires that you move ./hq from proxygen httpserver samples into the /python_interface/ folder

#Pre: a file name, e.g. "hello.txt"
#Post: True or false if the file was able to be downloaded or not
def request_file(file_name):
    return client_comm.get_request(file_name)

#Post: List of all available movies
def request_movie_list():
    return client_comm.get_request("/list_movies")

# Pre: Params is a list of parameters that start with "./hq", "-mode=client" etc. Example list: params = ["./hq", "-mode=client", "-path=/hello.txt"]
def custom_request(params):
    return client_comm.custom_get_request(params);
