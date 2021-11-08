
import subprocess

def get_request(file_name):
    program_name = "./hq"
    hq_mode = "-mode=client"
    file_path = "--path=/" + file_name
    storage_path = "-outdir=/home/axel/Downloads/"
    boll = subprocess.run([program_name, hq_mode, file_path, storage_path])
    print(boll)
