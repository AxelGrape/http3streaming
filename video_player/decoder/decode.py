import os
import subprocess
def decoder(path, si, ei, quality):
    quality1 = str(int(quality) + 1)

    if(len(si.lstrip('0')) == 0):
        return False, 'Invalid startindex'
        
    chnks = [str(item).zfill(len(ei)) for item in [*range(int(si.lstrip('0')), int(ei.lstrip('0'))+1)]]

    print("remove contents of out? (y/n)")
    subprocess.run("rm out/*", shell = True, check = True)



    if(os.path.isfile(path + "/dash_init_" + quality + ".m4s") & os.path.isfile(path + "/dash_init_" + quality1 + ".m4s")):
        try:
            subprocess.run( "cat " + path + "/dash_init_" + quality + ".m4s > out/all" + quality + ".m4s", shell = True, check = True)
            subprocess.run( "cat " + path + "/dash_init_" + quality1 + ".m4s > out/all" + quality1 + ".m4s", shell = True, check = True)
        except subprocess.CalledProcessError:
            print("OPS")

    
        for c in chnks:
            if(os.path.isfile(path + "/dash_chunk_" + quality + "_"+str(c)+".m4s") & os.path.isfile(path + "/dash_chunk_" + quality1 + "_"+str(c)+".m4s")):
                print(f'c is {c}')
                try:
                    subprocess.run( "cat $(ls -vx " + path + "/dash_chunk_" + quality + "_"+str(c)+".m4s) >> out/all" + quality + ".m4s", shell = True, check = True)
                    subprocess.run( "cat $(ls -vx " + path + "/dash_chunk_" + quality1 + "_"+str(c)+".m4s) >> out/all" + quality1 + ".m4s", shell = True, check = True)
                except subprocess.CalledProcessError:
                    print("O.P.S.I.E" + str(c))
            else:
                return False, f'chunk creation failed: {c}'

        subprocess.run("ffmpeg -i out/all" + quality + ".m4s -i out/all" + quality1 + ".m4s -c:v copy -c:a aac out/vid" + ei + ".mp4", shell = True, check = True)
        return True, "out/vid" + ei + ".mp4"
        
    else:
        return False, 'Init file failed'

def main():
    path = 'nature'
    startindex = '00001'
    slutindex = '00007'
    quality = '0'
    siri = decoder(path, startindex, slutindex, quality)

    print("Playing video")
    if siri[0]:
        subprocess.run("xdg-open " + siri[1], shell = True, check = True)
    else:
        print(siri[1])

if __name__ == "__main__":
    main()