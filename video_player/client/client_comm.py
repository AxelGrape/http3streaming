import subprocess
import client.file_handler
import os

def get_request(file_name, storage_path):
    program_name = "./hq"
    hq_mode = "-mode=client"
    file_path = "--path=/" + file_name
    store = "-outdir=" + storage_path
    subprocess.run([program_name, hq_mode, file_path, store])
    #print(program_name + hq_mode + file_path + storage_path)
    #print(f'\n detta är storage path{storage_path}\n')
    #return storage_path

def custom_get_request(params):
    subprocess.run(params)
