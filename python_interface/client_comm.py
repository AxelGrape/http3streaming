
import subprocess
import file_handler

def get_request(file_name):
    program_name = "./hq"
    hq_mode = "-mode=client"
    file_path = "--path=/" + file_name
    storage_path = "-outdir=/home/axel/Downloads/"
    subprocess.run([program_name, hq_mode, file_path, storage_path])

def custom_get_request(params):
    subprocess.run(params)
