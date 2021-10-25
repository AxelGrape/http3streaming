import os 
import ffmpeg_streaming
from ffmpeg_streaming import Formats

#path = 'var/media/video.mp4'
path_to_movies = 'var/media/'
path_output = 'var/media/dash.mpd'


#Checks if a file exists
def file_exists(file_name):
    return True if os.path.isfile(file_name) else False

#Creates a directory with the same name as the movie. minus the extension
def make_directory(movie_name):
    try: 
        new_directory = os.path.join(path_to_movies,os.path.splitext(movie_name)[0])
        os.mkdir(new_directory)
        return new_directory
    except OSError as error: 
        print(error)  
        return False

#Returns all movies in a list, with file extensions
def get_movie_list():
    return os.listdir(path_to_movies)

#interface to choose a movie from the directory
def choose_movie():
    movie_list_no_extensions = get_movie_list()

    for movie in movie_list_no_extensions:
        print(movie)

    choice = int(input(f'Choose a movie, ordered from 1 to {len(movie_list_no_extensions)}\n'))
    print(f'Movie : {movie_list_no_extensions[choice - 1]}')

    return movie_list_no_extensions[choice - 1]

#Encodes a given file, located in file_name path and stores it in a folder in output_name
def encode_video(file_name, output_name):
    if(file_exists(file_name)):
        video = ffmpeg_streaming.input(file_name)
        dash = video.dash(Formats.h264())
        dash.auto_generate_representations()
        output_name = os.path.join(output_name, 'dash.mpd')
        dash.output(output_name)
        print("Encoding done - No promise of success")
    else:
        print("File does not exist")

def encode_and_store_video():
    movie_name = choose_movie()
    movie_path = os.path.join(path_to_movies, movie_name)
    output_path = make_directory(movie_name)

    if(output_path != False):
        print("Directory created!")
        print(output_path)
        print(movie_path)
        encode_video(movie_path ,output_path)
    else:
        print("Directory failed!")
