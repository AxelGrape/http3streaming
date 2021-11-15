import os
import subprocess
def decoder(path, si, ei, quality):
    quality1 = str(int(quality) + 1)

    if(len(si.lstrip('0')) == 0):
        return False, 'Invalid startindex'
        
    #rnge = [*range(int(si.lstrip('0')), int(ei.lstrip('0')))]
    chnks = [str(item).zfill(len(ei)) for item in [*range(int(si.lstrip('0')), int(ei.lstrip('0'))+1)]]

    print("remove contents of out? (y/n)")
    #if input() == "y":
    subprocess.run("rm out/*", shell = True, check = True)


#os.system( "cat $(ls -vx sample_video/dash_init_*.m4s) > sampleF.mp4")
#os.system( "cat $(ls -vx sample_video/dash_chunk_*.m4s) >> sampleF.mp4")
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



    #os.system( "cat " + path + "/dash_init_" + quality + ".m4s $(ls -vx " + path + "/dash_chunk_" + quality + "_0000[" + si + "-" + ei + "].m4s) > out/all" + quality + ".m4s")
    #os.system( "cat " + path + "/dash_init_" + quality1 + ".m4s $(ls -vx " + path + "/dash_chunk_" + quality1 + "_0000[" + si + "-" + ei + "].m4s) > out/all" + quality1 + ".m4s")
    #os.system( "cat SampleVideo_1280x720_10mb/dash_init_0.m4s $(ls -vx SampleVideo_1280x720_10mb/dash_chunk_0_0000[0-3].m4s) > out/all0.m4s")
    #os.system( "cat SampleVideo_1280x720_10mb/dash_init_1.m4s $(ls -vx SampleVideo_1280x720_10mb/dash_chunk_1_0000[0-3].m4s) > out/all1.m4s")

    #os.system( "cat SampleVideo_1280x720_10mb/dash_init_0.m4s $(ls -vx SampleVideo_1280x720_10mb/dash_chunk_0_0000[4-7].m4s) > out/all0_.m4s")
    #os.system( "cat SampleVideo_1280x720_10mb/dash_init_1.m4s $(ls -vx SampleVideo_1280x720_10mb/dash_chunk_1_0000[4-7].m4s) > out/all1_.m4s")

    #os.system("ffmpeg -i out/all5.m4s -c copy out/Vid5.mp4")
        subprocess.run("ffmpeg -i out/all" + quality + ".m4s -i out/all" + quality1 + ".m4s -c:v copy -c:a aac out/vid" + ei + ".mp4", shell = True, check = True)
    #os.system("ffmpeg -i out/all0_.m4s -i out/all1_.m4s -c:v copy -c:a aac out/all01_.mp4")
        return True, "out/vid" + ei + ".mp4"
        

    #os.system("printf \"file '%s'\n\" out/*.mp4 > mylist.txt")
    #os.system("ffmpeg -f concat -i mylist.txt -c copy out/tmp.mp4")
    #os.system("ffmpeg -i out/tmp.mp4 -c copy out/all01.mp4 -y")
    #echo \"y\" | 
    #os.system("xdg-open out/all01.mp4")
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

#print("Play vid? (y/n)")
#if input() == "y":
# os.system("xdg-open out/both01_0347.mp4")

#os.system( "cat $(ls -vx sample_video/dash_init_*.m4s) > sampleF.mp4")
#os.system( "cat $(ls -vx sample_video/dash_chunk_*.m4s) >> sampleF.mp4")


#os.system( "cat sample_video/dash_init_0.m4s > sample00.mp4")
#os.system( "cat $(ls -vx sample_video/dash_chunk_0_*.m4s) >> sample00.mp4")

#os.system( "cat sample_video/dash_init_1.m4s >> sample00.mp4")
#os.system( "cat $(ls -vx sample_video/dash_chunk_1_*.m4s) >> sample00.mp4")

#os.system( "cat sample_video/dash_init_2.m4s >> sample00.mp4")
#os.system( "cat $(ls -vx sample_video/dash_chunk_2_*.m4s) >> sample00.mp4")

#os.system( "cat sample_video/dash_init_3.m4s >> sample00.mp4")
#os.system( "cat $(ls -vx sample_video/dash_chunk_3_*.m4s) >> sample00.mp4")

#os.system( "cat sample_video/dash_chunk_0_00001.m4s >> sample00.mp4")
#os.system( "cat sample_video/dash_chunk_0_00002.m4s >> sample00.mp4")
#os.system( "cat sample_video/dash_chunk_0_00003.m4s >> sample00.mp4")
#os.system( "cat sample_video/dash_chunk_0_00004.m4s >> sample00.mp4")
#os.system( "cat hbo/dash_chunk_1_00001.m4s >> hbo.mp4")
#os.system( "cat hbo/dash_chunk_1_00002.m4s >> hbo.mp4")
#os.system( "cat hbo/dash_chunk_2_00001.m4s >> hbo.mp4")
#os.system( "cat hbo/dash_chunk_3_00001.m4s >> hbo.mp4")
#os.system( "cat hbo/dash_chunk_3_00002.m4s >> hbo.mp4")
#os.system( "cat hbo/dash_chunk_4_00001.m4s >> hbo.mp4")
#os.system( "cat hbo/dash_chunk_5_00001.m4s >> hbo.mp4")
#os.system( "cat hbo/dash_chunk_5_00002.m4s >> hbo.mp4")
#os.system( "cat hbo/dash_chunk_6_00001.m4s >> hbo.mp4")