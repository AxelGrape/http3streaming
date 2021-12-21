import subprocess
import os

def get_request(file_name, storage_path, host_ip):
    program_name = "./team"
    hq_mode = "-mode=client"
    file_path = "--path=/" + file_name
    store = "-outdir=" + storage_path
    host = "--host=" + host_ip
    subprocess.run([program_name, hq_mode, file_path, store, host],  stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
