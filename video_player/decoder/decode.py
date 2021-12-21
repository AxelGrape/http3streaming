import os
import subprocess

def test_path():
    subprocess.run(["ls"])

def decoder(path, si, ei, quality, file_name):
    #quality is vid, quality+1 is audio.
    quality1 = str(int(quality) + 1)

    #Set output directory for audio/video .m4s files and final .mp4 file
    output_directory = f'vid/{file_name}/out'
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)

    #Check if start index is all zeroes. Return with False if all zeroes.
    if(len(si.lstrip('0')) == 0):
        return False, 'Invalid startindex'

    #Create a list with numbers from start-index to end-index, eg. 00005, 00006, ... , 00010.
    chnks = [str(item).zfill(len(ei)) for item in [*range(int(si.lstrip('0')), int(ei.lstrip('0'))+1)]]

    #Clear output directory. If already empty, print exception and continue.
    try:
        subprocess.run("rm " + output_directory + "/all*", shell = True, check = True, stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        hola = "command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output)

    #Check if init files exist, if not then return with False
    if(os.path.isfile(path + "/dash_init_" + quality + ".m4s") & os.path.isfile(path + "/dash_init_" + quality1 + ".m4s")):
        #Write video & audio init files to new temporary .m4s files in output directory
        try:
            subprocess.run( "cat " + path + "/dash_init_" + quality + ".m4s > " + output_directory + "/all" + quality + ".m4s", shell = True, check = True)
            subprocess.run( "cat " + path + "/dash_init_" + quality1 + ".m4s > " + output_directory + "/all" + quality1 + ".m4s", shell = True, check = True)
        except subprocess.CalledProcessError:
            print("OPS")

        #for each chunk between start-index and end-index: append their content to the temporary .m4s file created above in the output directory.
        for c in chnks:
            if(os.path.isfile(path + "/dash_chunk_" + quality + "_"+str(c)+".m4s") & os.path.isfile(path + "/dash_chunk_" + quality1 + "_"+str(c)+".m4s")):
                #print(f'c is {c}')
                try:
                    subprocess.run( "cat $(ls -vx " + path + "/dash_chunk_" + quality + "_"+str(c)+".m4s) >> " + output_directory + "/all" + quality + ".m4s", shell = True, check = True)
                    subprocess.run( "cat $(ls -vx " + path + "/dash_chunk_" + quality1 + "_"+str(c)+".m4s) >> " + output_directory + "/all" + quality1 + ".m4s", shell = True, check = True)
                except subprocess.CalledProcessError:
                    print("O.P.S.I.E" + str(c))
            else:
                #if an .m4s chunk file doesn't exist or fails in any other way to append, then return False
                return False, f'chunk creation failed: {c}'

        #copy and merge complete audio and video .m4s files into one .mp4 file with ffmpeg into output directory
        subprocess.run("ffmpeg -i " + output_directory + "/all" + quality + ".m4s -i " + output_directory + "/all" + quality1 + ".m4s -c:v copy -c:a aac " + output_directory + "/vid" + ei + ".mp4 -hide_banner -loglevel error", shell = True, check = True)

        #removes temporary .m4s files
        subprocess.run("rm " + output_directory + "/*.m4s" , shell = True, check = True, stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

        return True, output_directory + "/vid" + ei + ".mp4"

    else:
        return False, 'Init file failed: ' + path + "/dash_init_" + quality + ".m4s"

def main():
    print("TODO")

if __name__ == "__main__":
    main()
