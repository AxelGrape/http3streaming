import subprocess
import client.file_handler
import os

def get_request(file_name):
    program_name = "./hq"
    hq_mode = "-mode=client"
    file_path = "--path=/" + file_name
    storage_path = "-outdir=" + os.getcwd()
    subprocess.run([program_name, hq_mode, file_path, storage_path])
    return os.getcwd() + "/" + file_name

def custom_get_request(params):
    subprocess.run(params)
